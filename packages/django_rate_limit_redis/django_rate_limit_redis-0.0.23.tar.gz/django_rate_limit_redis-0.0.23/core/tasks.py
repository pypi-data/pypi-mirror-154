from django.core import management
from django.db.models import Q
from django.utils import timezone

from core.management.commands.kafka_producer import PHKafkaProducer
from core.models import Branch
from core.models import KafkaMsg
from core.models import Order
from core.models import ReconciliationResidue
from core.models import ResidueHistory
from core.models import Store
from core.systems.pharmzakaz import PharmZakazSystem
from project.celery import app
from project.celery import DEFAULT_QUEUE


@app.task(ignore_result=True)
def send_all_nomenclature(*args, **kwargs):
    PharmZakazSystem().update_all_nomenclature()


@app.task(ignore_result=True)
def update_all_store(*args, **kwargs):
    qs = Store.objects.filter(sended=False)\
        .exclude(Q(branch=None) | Q(building='') | Q(city=''))
    if qs.exists():
        PharmZakazSystem().update_all_store(qs=qs)


@app.task(ignore_result=True)
def create_new_store(*args, **kwargs):
    qs = Store.objects.filter(
        store_info_id=None,
        sended=False
    ).exclude(Q(branch=None) | Q(building='') | Q(city=''))
    if qs.exists():
        PharmZakazSystem().create_store(qs=qs)


@app.task(ignore_result=True)
def update_all_residues_batch(*args, **kwargs):
    PharmZakazSystem().update_all_residues_batch()
    PharmZakazSystem().residue_reconciliation()


@app.task(ignore_result=True)
def send_msg_to_kafka(*args, **kwargs):
    qs = KafkaMsg.objects.all()
    kafka = PHKafkaProducer()
    for obj in qs:
        # TODO могут быть проблемы из за асинхрона внутри,
        #  в колбэки могут не попасть данные если забыть producer.flush()
        kafka.send(obj.topic, obj.msg, obj.data_key, obj.recipient, obj.dict_obj)
        obj.delete()


@app.task(ignore_result=True)
def get_new_orders(*args, **kwargs):
    PharmZakazSystem().get_new_list_orders()


@app.task(ignore_result=True)
def get_new_orders_with_branch(*args, **kwargs):
    PharmZakazSystem().get_list_orders_with_branch(**kwargs)


@app.task(ignore_result=True)
def get_new_orders_assync(*args, **kwargs):
    add_params = {'status': 'new'}
    qs = Branch.objects.exclude(warehouse_id=None)
    for branch in qs:
        get_new_orders_with_branch.apply_async(
            queue=DEFAULT_QUEUE,
            kwargs={
                'inn': branch.inn,
                'add_params': add_params
            }
        )


@app.task(ignore_result=True)
def send_orders_to_pz(*args, **kwargs):
    qs = Order.objects.filter(sended_to_pz=False).exclude(document_number=None)
    order_ids = list(qs.values_list('order_id', flat=True))
    for order_id in order_ids:
        PharmZakazSystem().order_update(order_id)


@app.task(ignore_result=True)
def send_invoice_to_pz(*args, **kwargs):
    PharmZakazSystem().create_invoice()


@app.task(ignore_result=True)
def update_invoice_to_pz(*args, **kwargs):
    PharmZakazSystem().update_invoice()


@app.task(ignore_result=True)
def send_warehouses_to_pz(*args, **kwargs):
    PharmZakazSystem().send_warehouses()


@app.task(ignore_result=True)
def get_new_legal_entities_requests(*args, **kwargs):
    PharmZakazSystem().get_new_legal_entities()
    PharmZakazSystem().send_legal_entities_to_1C()


@app.task(ignore_result=True)
def get_send_legal_entities_onboarded(*args, **kwargs):
    PharmZakazSystem().send_onboarded_legal_entities()


@app.task(ignore_result=True)
def clearing_old_records_residues_history(*args, **kwargs):
    timedelta = timezone.now() - timezone.timedelta(days=7)
    ResidueHistory.objects.filter(created_at__lte=timedelta)[:1000].delete()
    ReconciliationResidue.objects.filter(created_at__lte=timedelta)[:1000].delete()


@app.task(ignore_result=True)
def ldap_auth_users_sync(*args, **kwargs):
    management.call_command('ldap_sync_users')
