import json
import uuid

from api.serializers import PositionSerializer
from api.serializers import ResidueSerializer
from jinja2 import Environment
from jinja2 import PackageLoader
from rest_framework import status

from django.conf import settings
from django.db.models import Max
from django.db.models import Q
from django.utils import timezone

from core.async_mode import AsyncPool
from core.conf import Settings
from core.consts import ORDER_DATA_KEY
from core.models import Branch
from core.models import ErrorsRequest
from core.models import Invoice
from core.models import KafkaMsg
from core.models import LegalEntity
from core.models import LegalEntityOnboarded
from core.models import Nomenclature
from core.models import Order
from core.models import Position
from core.models import ReconciliationResidue
from core.models import Residue
from core.models import ResidueHistory
from core.models import Store
from core.systems.pharmzakaz.requests import InvoicesRequest
from core.systems.pharmzakaz.requests import LegalEntitiesRequest
from core.systems.pharmzakaz.requests import OrdersRequest
from core.systems.pharmzakaz.requests import SKURequest
from core.systems.pharmzakaz.requests import StoresRequest
from core.systems.pharmzakaz.requests import WarehousesRequest
from core.tg_bot import PharmZakazTelegramBot
from core.utils import grouper
from core.utils import parse_datetime


class PharmZakazSystem:
    def __init__(self):
        self.conf = Settings()

    def save_error_request(self, errors, status_code, request_name):
        try:
            errors = errors.json()
        except Exception:
            pass
        ErrorsRequest.objects.create(
            error=str(errors)[:500],
            status_code=status_code,
            request=request_name
        )

    def parse_errors(self, string, status_code):
        """'Ean13=4601969009620 sku does not exists.'"""

        if 'Ean13=' in string:
            string = string.replace(' sku does not exists.', '')
            return string.replace('Ean13=', '')
        else:
            self.save_error_request(string, status_code, 'PharmZakazSystem.parse_errors')

    def update_all_nomenclature(self, qs=None):
        if not qs:
            qs = Nomenclature.objects.exclude(ean13="")
        else:
            qs = qs.exclude(ean13="")
        sku_list = []
        for group in grouper(qs, 100):
            for nomenclature in group:
                sku_one = {
                    "GTIN": nomenclature.gtin,
                    "name": nomenclature.name,
                    "extSkuId": nomenclature.code,
                    "ean13": nomenclature.ean13
                }
                sku_list.append(sku_one)
            request_obj = SKURequest()
            response = request_obj.sku_update_sku_list(sku_list=sku_list)
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                errors = response.json().get("errors")
                if not errors:
                    self.save_error_request(response.json(), response.status_code,
                                            'PharmZakazSystem.update_all_nomenclature')
                else:
                    for error in errors:
                        ean13 = self.parse_errors(error, response.status_code)
                        qs = Nomenclature.objects.filter(ean13=ean13)
                        for nomenclature in qs:
                            nomenclature.comment = error
                            nomenclature.sended = False
                            nomenclature.save()
            elif response.status_code == status.HTTP_502_BAD_GATEWAY:
                return
            else:
                results = response.json().get("results")
                errors = response.json().get("errors")

                for sku in results:
                    nomenclature = Nomenclature.objects.get(code=sku.get("extSkuId"))
                    nomenclature.sended = True
                    nomenclature.sended_at = timezone.now()
                    nomenclature.comment = None
                    nomenclature.save()

                for error in errors:
                    ean13 = self.parse_errors(error, response.status_code)
                    qs = Nomenclature.objects.filter(ean13=ean13)
                    for nomenclature in qs:
                        nomenclature.comment = error
                        nomenclature.sended = False
                        nomenclature.save()

    # TODO Убрать или переделать
    def get_sku_residues_list(self):
        ean13_list = Nomenclature.objects.all().distinct('ean13').values_list('ean13', flat=True)
        warehouse_id_list = Branch.objects.all().exclude(warehouse_id=None).values_list('warehouse_id', flat=True)
        all_residue = []
        for warehouse_id in warehouse_id_list:
            for ean13 in ean13_list:
                r = SKURequest().sku_residues_list(ean13=ean13, warehouseId=warehouse_id)
                print(r.json())
                all_residue.append(r.json())
        print(all_residue)
        return all_residue

    def update_all_residues_batch(self, ean13_list=None, update_diff=True):
        if not ean13_list:
            ean13_list = Residue.objects.all().distinct('ean13').values_list('ean13', flat=True)

        responses = []
        pool = None
        if self.conf.USE_ASYNC:
            pool = AsyncPool(
                pool_size=self.conf.ASYNC_POOL_SIZE_REQUEST,
                use_process=self.conf.USE_ASYNC_PROCESS
            )

        for ean13 in ean13_list:
            residue_qs = Residue.objects.filter(ean13=ean13)

            serializer = ResidueSerializer(residue_qs, many=True)
            sku_residues_list = serializer.data
            if pool:
                pool.apply_async(self.update_residue_for_ean13, ean13, sku_residues_list)
            else:
                response = self.update_residue_for_ean13(ean13, sku_residues_list)
                responses.append(response)

        if pool:
            responses = pool.get()

        for response in responses:
            if response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]:
                results = response.json().get('results')
                errors = response.json().get("errors")
                for result in results:
                    Residue.objects.filter(ean13=result.get('ean13')).update(sended=True, sended_at=timezone.now())

                if errors:
                    self.save_error_request(errors, response.status_code,
                                            'PharmZakazSystem.update_all_residues_batch')
            else:
                self.save_error_request(response, response.status_code,
                                        'PharmZakazSystem.update_all_residues_batch')
        if update_diff:
            self.update_all_residues_batch_diff()

    def update_all_residues_batch_diff(self):
        inn_list = Branch.objects.all().values_list('inn', flat=True)
        for inn in inn_list:
            qs = self.get_diff_residues(inn)
            if not qs:
                continue
            ean13_list = qs.distinct('ean13').values_list('ean13', flat=True)
            for ean13 in ean13_list:
                residue_qs = ResidueHistory.objects.filter(ean13=ean13)

                serializer = ResidueSerializer(residue_qs, many=True)
                sku_residues_list = serializer.data

                response = SKURequest().sku_residues_update_residues_list(
                    ean13=ean13,
                    sku_residues_list=sku_residues_list
                )
                if response.status_code == status.HTTP_200_OK:
                    residue_qs.update(sended=True, sended_at=timezone.now())
                    errors = response.json().get("errors")
                    if errors:
                        self.save_error_request(response.json(), response.status_code,
                                                'PharmZakazSystem.update_all_residues_batch')
                else:
                    self.save_error_request(response, response.status_code,
                                            'PharmZakazSystem.update_all_residues_batch')

    def get_diff_residues(self, inn):
        qs_history_batch = ResidueHistory.objects.filter(warehouse_ext_id=inn).exclude(rest_time=None)
        if not qs_history_batch:
            return None
        last_uid_batch = qs_history_batch.latest('rest_time').uid_batch
        qs_history = ResidueHistory.objects.filter(warehouse_ext_id=inn, uid_batch=last_uid_batch)
        qs_residue = Residue.objects.filter(warehouse_ext_id=inn)
        qs_result = qs_history.exclude(
            ean13__in=qs_residue.values('ean13'),
            nomenclature__in=qs_residue.values('nomenclature'),
            series__in=qs_residue.values('series'),
        ).extra(select={'quantity': 0})
        return qs_result

    def create_store(self, qs=None):
        if not qs:
            qs = Store.objects.filter(sended=False) \
                .exclude(Q(branch=None) | Q(building='') | Q(city=''))
        for store in qs:
            branch = Branch.objects.get(inn=store.branch).warehouse_id
            request_obj = StoresRequest()
            response = request_obj.stores_create(
                store.inn,
                store.legal_name,
                store.fias_id,
                store.fias_code,
                store.federal_district,
                store.region,
                store.regional_district,
                store.city,
                store.street,
                store.building,
                store.full_address,
                store.has_contract,
                store.black_list,
                store.payment_delay,
                store.pos_ext_id,
                warehouseId=branch
            )
            if response.status_code == status.HTTP_201_CREATED:
                result = response.json()
                store.sended = True
                store.sended_at = timezone.now()
                store.store_info_id = result.get('storeInfoId')
                store.created = result.get('created')
                store.warehouses = result.get('warehouses')
                store.save()
            elif response.status_code == status.HTTP_502_BAD_GATEWAY:
                return
            else:
                self.save_error_request(response, response.status_code, 'PharmZakazSystem.create_store')

    def update_one_store(self, store_info_id=None, pos_ext_id=None, store=None):
        if not store:
            try:
                store = Store.objects.get(Q(store_info_id=store_info_id) | Q(pos_ext_id=pos_ext_id))
            except Store.DoesNotExist:
                if store_info_id:
                    self.read_one_store(store_info_id)
                    store = Store.objects.get(store_info_id=store_info_id)
                elif pos_ext_id:
                    raise Exception(f"Адрес с store_info_id:{store_info_id} "
                                    f"или pos_ext_id:{pos_ext_id} не найден в БД")

            if not store.branch or not store.building or not store.city:
                raise Exception("Нельзя обновить адрес без Склада/Строения/Города")

        branch_qs = Branch.objects.filter(inn=store.branch)
        if not branch_qs.exists():
            self.save_error_request('Branch not found', 0, 'PharmZakazSystem.update_one_store')
            return

        branch = branch_qs.first().warehouse_id
        request_obj = StoresRequest()
        response = request_obj.stores_partial_update(
            store.store_info_id,
            store.inn,
            store.legal_name,
            store.fias_id,
            store.fias_code,
            store.federal_district,
            store.region,
            store.regional_district,
            store.city,
            store.street,
            store.building,
            store.full_address,
            store.has_contract,
            store.black_list,
            store.payment_delay,
            store.pos_ext_id,
            warehouseId=branch
        )
        if response.status_code == status.HTTP_201_CREATED or response.status_code == status.HTTP_200_OK:
            result = response.json()
            self.update_store_in_db(result)
        elif response.status_code == status.HTTP_502_BAD_GATEWAY:
            return
        else:
            self.save_error_request(response, response.status_code, 'PharmZakazSystem.update_one_store')

    def update_all_store(self, qs=None):
        if not qs:
            qs = Store.objects.all()
        qs = qs.exclude(Q(branch=None) | Q(building='') | Q(city='') | Q(store_info_id=None))
        for store in qs:
            self.update_one_store(store=store)

    def update_store_in_db(self, item):
        branch = Branch.objects.get(warehouse_id=item.get('warehouses')[0].get('warehouseId'))
        store_info_id = int(item.get('storeInfoId'))
        update_fields = dict(
            store_info_id=store_info_id,
            inn=item.get("inn"),
            legal_name=item.get("legalName"),
            fias_id=item.get("fiasId"),
            fias_code=item.get("fiasCode"),
            federal_district=item.get("federalDistrict"),
            region=item.get("region"),
            regional_district=item.get("regionalDistrict"),
            city=item.get("city"),
            street=item.get("street"),
            building=item.get("building"),
            full_address=item.get("fullAddress"),
            has_contract=item.get("hasContract"),
            black_list=item.get("isBlacklist"),
            payment_delay=item.get("paymentDelay"),
            pos_ext_id=item.get("posExtId"),
            branch=branch.inn,
            created=item.get('created'),
            warehouses=item.get('warehouses'),
            sended=True,
        )
        Store.objects.update_or_create(
            pos_ext_id=item.get('posExtId'),
            store_info_id=store_info_id,
            defaults=update_fields
        )

    def read_list_stores(self, inn=None):
        branches = Branch.objects.exclude(warehouse_id=None)
        if inn:
            branches = branches.filter(inn=inn)
        for branch in branches:
            request_obj = StoresRequest()
            response = request_obj.stores_list(warehouseId=branch.warehouse_id)
            results = response.json().get('results')
            for item in results:
                self.update_store_in_db(item)

    def read_one_store(self, storeInfoId):
        request_obj = StoresRequest()
        response = request_obj.stores_read(storeInfoId)
        item = response.json()
        self.update_store_in_db(item)

    def send_warehouses(self, qs=None):
        if not qs:
            qs = Branch.objects.filter(sended=False)
        qs = qs.filter(warehouse_id=None)
        for branch in qs:
            request_obj = WarehousesRequest()
            response = request_obj.warehouses_create(
                name=branch.name,
                address=branch.address,
                extId=branch.inn,
            )
            if response.status_code == status.HTTP_201_CREATED:
                result = response.json()
                branch.sended = True
                branch.sended_at = timezone.now()
                branch.ext_data = result.get('extData')
                branch.warehouse_id = result.get('warehouseId')
                branch.save()
            else:
                self.save_error_request(response, response.status_code, 'PharmZakazSystem.send_warehouses')

    def update_warehouses(self, qs=None):
        if not qs:
            qs = Branch.objects.filter(sended=False)
        qs = qs.exclude(warehouse_id=None)
        for branch in qs:
            request_obj = WarehousesRequest()
            response = request_obj.warehouses_partial_update(
                branch.warehouse_id,
                name=branch.name,
                address=branch.address,
                extId=branch.inn,
                extData=branch.ext_data
            )
            if response.status_code == status.HTTP_200_OK:
                branch.sended = True
                branch.sended_at = timezone.now()
                branch.save()
            else:
                self.save_error_request(response, response.status_code, 'PharmZakazSystem.update_warehouses')

    def get_warehouses(self):
        request_obj = WarehousesRequest()
        response = request_obj.warehouses_list()
        if response.status_code == status.HTTP_200_OK:
            results = response.json().get('results')
            for warehouse in results:
                update_fields = dict(
                    name=warehouse.get("name"),
                    address=warehouse.get("address"),
                    inn=warehouse.get("extId"),
                    ext_data=warehouse.get("extData"),
                    sended_at=timezone.now(),
                    warehouse_id=warehouse.get("warehouseId"),
                    sended=True,
                )
                Branch.objects.update_or_create(
                    inn=warehouse.get('extId'),
                    defaults=update_fields
                )

    def get_dict_fields_positions(self, order, position):
        update_fields = dict(
            order=order,
            position_id=position.get('positionId'),
            gtin=position.get('gtin'),
            ean13=position.get('ean13'),
            series=position.get('series'),
            item_id=position.get('itemId'),
            quantity=position.get('quantity'),
            price=position.get('price'),
            vat=position.get('vat'),
            expiration_date=position.get('expirationDate'),
            ext_id=position.get('extId'),
            invoice_num=position.get('invoiceNum'),
            warehouse_ext_id=position.get('warehouseExtId'),
        )
        return update_fields

    def _get_pos_ext_id(self, store_ext_id):
        qs = Store.objects.filter(store_info_id=store_ext_id)
        if qs.exists():
            store_ext_id = qs.first().pos_ext_id
        return store_ext_id

    def _get_store_ext_id(self, pos_ext_id):
        qs = Store.objects.filter(pos_ext_id=pos_ext_id)
        if qs.exists():
            pos_ext_id = qs.first().store_ext_id
        return pos_ext_id

    def get_dict_fields_order(self, order, count_positions, warehouse_ext_id=None):
        update_fields = dict(
            order_id=order.get('orderId'),
            status=order.get('status'),
            store_ext_id=order.get('posExtId'),
            created=order.get('created'),
            updated=order.get('updated'),
            total_sum=order.get('totalSum'),
            vat_sum=order.get('vatSum'),
            count_positions=count_positions,
            warehouse_ext_id=warehouse_ext_id
        )
        return update_fields

    def get_last_order_with_branch(self, branch):
        qs = Order.objects.filter(warehouse_ext_id=branch.inn)
        if qs.exists():
            return qs.latest('created').created.date()
        else:
            return None

    def get_list_orders(self, qs=None, add_params=None):
        if not qs:
            qs = Branch.objects.exclude(warehouse_id=None)
        for branch in qs:
            self.get_list_orders_with_branch(branch=branch, add_params=add_params)

    def get_list_orders_with_branch(self, inn=None, add_params=None, branch=None):
        if not branch and inn:
            qs = Branch.objects.exclude(warehouse_id=None).filter(inn=inn)
            if not qs.exists():
                return None
            branch = qs.first()

        if add_params:
            last_order = self.get_last_order_with_branch(branch)
            if last_order:
                add_params.update({'created_gte': last_order})

        request_obj = OrdersRequest()
        response = request_obj.orders_list(warehouseId=branch.warehouse_id, add_params=add_params)

        while True:
            status_code = response.status_code
            if status_code == status.HTTP_200_OK:
                order_list = []
                response = response.json()
                results = response.get('results')
                for order in results:
                    positions = order.get('positions')
                    count_positions = len(positions)
                    warehouse_ext_id = list({w.get("warehouseExtId") for w in positions})

                    if not warehouse_ext_id:
                        raise Exception(f'Не найден, либо найдено более одного склада по позициям заказа {order}')

                    warehouse_ext_id = warehouse_ext_id[0]
                    update_fields = self.get_dict_fields_order(order, count_positions, warehouse_ext_id)

                    order_obj, create = Order.objects.get_or_create(
                        order_id=order.get('orderId'),
                        defaults=update_fields
                    )
                    if create:
                        order_list.append(order_obj.order_id)
                    for position in positions:
                        update_positions_fields = self.get_dict_fields_positions(order_obj, position)
                        Position.objects.get_or_create(
                            order=order_obj.order_id,
                            position_id=position.get('positionId'),
                            gtin=position.get('gtin'),
                            ean13=position.get('ean13'),
                            series=position.get('series'),
                            ext_id=position.get('extId'),
                            defaults=update_positions_fields
                        )
                if order_list:
                    self.save_msg_order_after_download(order_list)
                next_page = response.get('next')
                if next_page:
                    response = request_obj.next(next_page)
                else:
                    break
            else:
                break

    def get_new_list_orders(self, qs=None, add_params=None):
        add_params = {'status': 'new'}
        self.get_list_orders(add_params=add_params)

    def order_update(self, order_id, order_status=None):
        order_obj = Order.objects.get(order_id=order_id)
        all_positions_qs = Position.objects.filter(order_id=order_id)

        refusal_qs = all_positions_qs.filter(info_received=False).extra(select={'quantity': 0})
        positions_qs = all_positions_qs.filter(info_received=True)

        if not order_status:
            order_status = order_obj.status

        serializer = PositionSerializer(refusal_qs, many=True)
        refusal_list = serializer.data

        serializer = PositionSerializer(positions_qs, many=True)
        positions_list = serializer.data

        result_positions_list = positions_list + refusal_list

        request_obj = OrdersRequest()
        response = request_obj.orders_partial_update(
            orderId=order_id,
            status=order_status,
            positions=result_positions_list
        )

        if response.status_code == status.HTTP_200_OK:
            result = response.json()
            positions = result.get('positions')

            update_fields = self.get_dict_fields_order(result, len(positions))
            update_fields.pop('warehouse_ext_id', None)
            update_fields.pop('order_id', None)

            for attr, value in update_fields.items():
                setattr(order_obj, attr, value)

            order_obj.save()

            for position in positions:
                position_id = position.get('positionId')
                update_positions_fields = self.get_dict_fields_positions(order_id, position)
                update_positions_fields.pop('ext_id', None)
                if refusal_qs.exists():
                    update_fields.pop('quantity', None)
                positions_qs.filter(position_id=position_id).update(**update_positions_fields)
        else:
            self.save_error_request(response, response.status_code,
                                    'PharmZakazSystem.order_update')

    def get_template(self, template_name: str):
        env = Environment(loader=PackageLoader('core', 'jinja_template'))
        # добавление своего функции-фильтра в Environment
        env.filters['jsonify'] = json.dumps

        # Template file at ./core/jinja_template/msg_template.json
        return env.get_template(f'{template_name}.json')

    def _generate_msg_template(self, recipient, data_key: str, body: list):
        '''
        "{{ page.msg_id }}" "Идентификатор" - Уникальный гуид каждого сообщения
        "{{ page.sender }}" "Отправитель" - 3 символа базы ФЗ
        "{{ page.recipient }}" "Получатель" - Префикс ИБ получателя
        "{{ page.sender_server }}" "Сервер" - Сервер отправителя(stage/prod)
        "{{ page.sender_db }}" "БазаДанных" - Название БД отправителя (неограничено, в разумных пределах)
        "{{ page.data_key }}" "КлючДанных" - Ключ для 1С, для заказов "ЗаказФЗ"
        '''

        template = self.get_template('msg_template')

        msg = {
            'msg_id': f'{uuid.uuid4()}',
            'sender': f'{settings.DATA_BASE_ABBR}',
            'recipient': f'{recipient}',
            'sender_server': f'pharmzakaz.{settings.ENV_TYPE}',
            'sender_db': f'{settings.DATA_BASE_ABBR}',
            'data_key': f'{data_key}',
        }
        return template.render(page=msg, body=body)

    def _generate_order_template(self, qs):
        template = self.get_template('order_template')
        positions_list = []
        order_ids_list = []
        for order in qs:
            positions_qs = Position.objects.filter(order=order.order_id)
            position_num = 0
            order_ids_list.append(order.order_id)
            for position in positions_qs:
                position_num += 1
                nomenclature = Nomenclature.objects.filter(code=position.ext_id).first()

                body = {
                    'order_id': order.order_id,
                    'store': self._get_pos_ext_id(order.store_ext_id),
                    'position_num': f'{position_num}',
                    'item_id': f'{position.item_id}',
                    'code': position.ext_id,
                    "quantity": position.quantity,
                    "name": nomenclature.name,
                    "expiration_date": str(position.expiration_date),
                    "price": float(position.price),
                    "mark": False
                }
                positions_list.append(body)
        data = template.render(body=positions_list)
        if not positions_list:
            return False, False
        return data, order_ids_list

    def save_msg_order(self, branch, orders_qs):
        orders_list, order_ids_list = self._generate_order_template(orders_qs)
        if orders_list:
            data_key = ORDER_DATA_KEY
            msg = self._generate_msg_template(branch.abbreviation, data_key, orders_list)
            msg = json.loads(msg)
            KafkaMsg.objects.create(
                topic=branch.target_topic_to_send,
                msg=msg,
                data_key=data_key,
                recipient=branch.abbreviation,
                dict_obj=dict(order_ids=order_ids_list)
            )

    def save_msg_order_with_branch(self):
        branches = Branch.objects.exclude(warehouse_id=None, abbreviation=None, )
        for branch in branches:
            orders_qs = Order.objects.filter(warehouse_ext_id=branch.inn, sended_to_one_c=False)
            for group in grouper(orders_qs, 10):
                self.save_msg_order(branch, group)
            orders_qs.update(sended_to_one_c=True)

    def save_msg_order_after_download(self, orders: list):
        orders_qs = Order.objects.filter(order_id__in=orders)
        branch_list = orders_qs.distinct('warehouse_ext_id').values_list('warehouse_ext_id', flat=True)
        branch_qs = Branch.objects.filter(inn__in=branch_list)
        for branch in branch_qs:
            orders_with_branch = orders_qs.filter(warehouse_ext_id=branch.inn)
            for group in grouper(orders_with_branch, 10):
                self.save_msg_order(branch, group)
            orders_with_branch.update(sended_to_one_c=True)

    def create_invoice(self, qs=None):
        if not qs:
            qs = Invoice.objects.filter(sended=False)
        qs = qs.filter(invoice_id=None)
        for invoice in qs:
            request_obj = InvoicesRequest()
            response = request_obj.invoices_create(
                invoiceNum=invoice.invoice_num,
                warehouseExtId=invoice.warehouse_ext_id,
                accepted=str(invoice.accepted.date()),
                delivered=str(invoice.delivered.date()),
                isAccept=invoice.is_accept,
                storeExtId=invoice.store_ext_id,
                skuExtId=invoice.sku_ext_id,
                deliveredQuantity=str(invoice.delivered_quantity),
                deliveredSum=str(invoice.delivered_sum),
            )
            status_code = response.status_code
            if status_code == status.HTTP_201_CREATED:
                result = response.json()
                invoice.invoice_id = result.get('invoiceId')
                invoice.sended = True
                invoice.sended_at = timezone.now()
                invoice.save()
            else:
                self.save_error_request(response, status_code, 'PharmZakazSystem.create_invoice')

    def get_invoice(self, invoice_id):
        request_obj = InvoicesRequest()
        response = request_obj.invoices_read(invoice_id)
        if response.status_code == status.HTTP_200_OK:
            return response.json()

    def list_invoice(self, qs=None):
        if not qs:
            qs = Branch.objects.exclude(warehouse_id=None)
        for branch in qs:
            request_obj = InvoicesRequest
            response = request_obj().invoices_list(warehouseId=branch.warehouse_id)
            while True:
                status_code = response.status_code
                if status_code == status.HTTP_200_OK:
                    response = response.json()
                    results = response.get('results')
                    for invoice in results:
                        branch = Branch.objects.get(warehouse_id=invoice.get("warehouseId"))
                        update_fields = dict(
                            invoice_num=invoice.get("invoiceNum"),
                            invoice_id=invoice.get("invoiceId"),
                            delivered=parse_datetime(invoice.get("delivered")),
                            created=parse_datetime(invoice.get("accepted")),
                            is_accept=invoice.get("isAccept"),
                            store_ext_id=invoice.get("storeExtId"),
                            sku_ext_id=invoice.get("skuExtId"),
                            delivered_quantity=invoice.get("deliveredQuantity"),
                            delivered_sum=invoice.get("deliveredSum"),
                            warehouse_ext_id=branch.inn,
                            sended=True,
                        )

                        Invoice.objects.update_or_create(
                            invoice_num=invoice.get("invoiceNum"),
                            invoice_id=invoice.get("invoiceId"),
                            sku_ext_id=invoice.get("skuExtId"),
                            defaults=update_fields
                        )
                    next_page = response.get('next')
                    if next_page:
                        response = request_obj().next(next_page)
                    else:
                        break
                else:
                    break

    def update_invoice(self, qs=None):
        if not qs:
            qs = Invoice.objects.filter(sended=False)
        qs = qs.exclude(invoice_id=None)
        for invoice in qs:
            request_obj = InvoicesRequest()
            response = request_obj.invoices_partial_update(
                invoice.invoice_id,
                invoiceNum=invoice.invoice_num,
                warehouseExtId=invoice.warehouse_ext_id,
                accepted=str(invoice.accepted.date()),
                delivered=str(invoice.delivered.date()),
                isAccept=invoice.is_accept,
                storeExtId=invoice.store_ext_id,
                skuExtId=invoice.sku_ext_id,
                deliveredQuantity=str(invoice.delivered_quantity),
                deliveredSum=str(invoice.delivered_sum),
            )
            status_code = response.status_code
            if status_code == status.HTTP_200_OK:
                result = response.json()
                invoice.invoice_id = result.get('invoiceId')
                invoice.sended = True
                invoice.sended_at = timezone.now()
                invoice.save()
            else:
                self.save_error_request(response, status_code, 'PharmZakazSystem.update_invoice')

    def get_new_legal_entities(self):
        latest_updated_date = LegalEntity.objects.all().aggregate(Max('updated'))['updated__max']
        add_params = {}
        if latest_updated_date:
            add_params['updatedGte'] = latest_updated_date.date

        legal_entity_request = LegalEntitiesRequest()
        response = legal_entity_request.legal_entities_requests_list(add_params)
        status_code = response.status_code
        results = response.json().get("results")

        if status_code == status.HTTP_200_OK:
            for legal_entity in results:
                pharm_zakaz_id = legal_entity['id']
                requested_inn = legal_entity['inn']
                legal_entity_db = LegalEntity.objects.filter(pharm_zakaz_id=pharm_zakaz_id).first()
                if not legal_entity_db:
                    LegalEntity.objects.create(
                        pharm_zakaz_id=pharm_zakaz_id,
                        inn=requested_inn,
                        opf=legal_entity['opf'],
                        legal_entity=legal_entity['legalEntity'],
                        address=legal_entity['address'],
                        full_name=legal_entity['fullName'],
                        position=legal_entity['position'],
                        basis_authority=legal_entity['basisAuthority'],
                        bic=legal_entity['bic'],
                        bank_account=legal_entity['bankAccount'],
                        bank=legal_entity['bank'],
                        kpp_bank=legal_entity['kppBank'],
                        correspondent_account=legal_entity['correspondentAccount'],
                        status=legal_entity['status'],
                        updated=legal_entity['updated'],
                    )

                elif legal_entity_db.status != legal_entity['status']:
                    legal_entity_db.status = legal_entity['status']
                    legal_entity_db.updated = legal_entity['updated']
                    legal_entity_db.sended_to_1c = False
                    legal_entity_db.save(update_fields=[
                        'status',
                        'updated',
                        'sended_to_1c',
                    ])

        else:
            self.save_error_request(results, status_code, 'PharmZakazSystem.get_new_legal_entities')

    def _generate_legal_entities_template(self, entities):
        template = self.get_template('legal_entities')
        data = template.render(elements=entities)
        return data

    def send_legal_entities_to_1C(self, entities=None):
        if not entities:
            # Взять все не отправленные LegalEntity
            entities = LegalEntity.objects.filter(sended_to_1c=False)
        if entities.exists():
            for entitie in entities:
                branches = Branch.objects.exclude(warehouse_id=None, abbreviation=None, )
                for branch in branches:
                    entities_template = self._generate_legal_entities_template([entitie])
                    msg = self._generate_msg_template(
                        recipient=branch.abbreviation,
                        data_key='КонтрагентыФЗ',
                        body=entities_template
                    )
                    msg = json.loads(msg)
                    KafkaMsg.objects.create(topic=branch.target_topic_to_send, msg=msg)
                    entitie.sended_to_1c = True
                    entitie.save()

    def send_onboarded_legal_entities(self, qs=None):
        legal_entity_request = LegalEntitiesRequest()

        if not qs:
            qs = LegalEntityOnboarded.objects.all()

        qs_leo = qs.filter(pharm_zakaz_id=None)  # так как не имеем ID, значит не отправляли
        for leo in qs_leo:
            response = legal_entity_request.legal_entities_create(
                inn=leo.inn,
                contactSignDate=str(leo.contact_sign_date),
                status=leo.status,
                statusUpdated=str(leo.status_updated),
                extId=leo.ext_id,
                comment=leo.comment,
            )
            if response.status_code == status.HTTP_201_CREATED:
                response_json = response.json()
                leo.sended_to_pz = True
                leo.sended_to_pz_at = timezone.now()
                leo.pharm_zakaz_id = response_json['id']
                leo.save(update_fields=['sended_to_pz', 'sended_to_pz_at', 'pharm_zakaz_id'])
            else:
                self.save_error_request(response.json(), response.status_code,
                                        'PharmZakazSystem.send_onboarded_legal_entities')

        qs_leo = qs.filter(sended_to_pz=False).exclude(pharm_zakaz_id=None)
        for leo in qs_leo:
            response = legal_entity_request.legal_entities_partial_update(
                id=leo.pharm_zakaz_id,
                inn=leo.inn,
                contactSignDate=str(leo.contact_sign_date),
                status=leo.status,
                statusUpdated=str(leo.status_updated),
                extId=leo.ext_id,
                comment=leo.comment,
            )
            if response.status_code == status.HTTP_200_OK:
                leo.sended_to_pz = True
                leo.sended_to_pz_at = timezone.now()
                leo.save(update_fields=['sended_to_pz', 'sended_to_pz_at'])
            else:
                self.save_error_request(response.json(), response.status_code,
                                        'PharmZakazSystem.send_onboarded_legal_entities')

    def update_residue_for_ean13(self, ean13, sku_residues_list,):
        sku_response = SKURequest().sku_residues_update_residues_list(
            ean13=ean13,
            sku_residues_list=sku_residues_list,
        )

        return sku_response

    def reset_all_residue(self, qs=None):
        if not qs:
            qs = Branch.objects.exclude(sended=False, warehouse_id=None)
        for branch in qs:
            request_obj = WarehousesRequest()
            request_obj.params = {"limit": 1000, "offset": 0, }
            response = request_obj.warehouses_residue_list(branch.warehouse_id)
            while True:
                if response.status_code == status.HTTP_200_OK:
                    response = response.json()
                    results = response.get('results')
                    pool = None
                    if self.conf.USE_ASYNC and len(results) > 0:
                        pool = AsyncPool(
                            pool_size=self.conf.ASYNC_POOL_SIZE_REQUEST,
                            use_process=self.conf.USE_ASYNC_PROCESS
                        )
                    for result in results:
                        if result.get('quantity') != 0:
                            from collections import OrderedDict
                            sku_residues_list = [
                                OrderedDict(
                                    ean13=result.get('ean13'),
                                    series=result.get('series'),
                                    warehouseExtId=result.get('warehouseExtId'),
                                    quantity=0,
                                    expirationDate=result.get('expirationDate'),
                                    extId=result.get('extId'),
                                    SkuExtId=result.get('SkuExtId'),
                                )
                            ]

                            if pool:
                                pool.apply_async(self.update_residue_for_ean13, result.get('ean13'), sku_residues_list)
                            else:
                                response = self.update_residue_for_ean13(result.get('ean13'), sku_residues_list)
                                errors = response.json()
                                if errors and response.status_code != status.HTTP_200_OK:
                                    self.save_error_request(errors, response.status_code,
                                                            'PharmZakazSystem.reset_all_residue')

                    if pool:
                        responses_list = pool.get()
                        for res in responses_list:
                            errors = res.json()
                            if errors and res.status_code != status.HTTP_200_OK:
                                self.save_error_request(errors, res.status_code,
                                                        'PharmZakazSystem.reset_all_residue')

                    next_page = response.get('next')
                    if next_page:
                        response = request_obj.next(next_page)
                    else:
                        break
                else:
                    self.save_error_request(response, response.status_code, 'PharmZakazSystem.send_warehouses')
                    break

    def residue_reconciliation(self, qs=None):
        uid_reconciliation = str(uuid.uuid4())
        is_error = False
        if not qs:
            qs = Branch.objects.exclude(sended=False, warehouse_id=None)
        for branch in qs:
            request_obj = WarehousesRequest()
            request_obj.params = {"limit": 1000, "offset": 0, }
            response = request_obj.warehouses_residue_list(branch.warehouse_id)
            residue_list = []
            while True:
                status_code = response.status_code
                if status_code == status.HTTP_200_OK:
                    response = response.json()
                    results = response.get('results')

                    residue_list += results

                    next_page = response.get('next')
                    if next_page:
                        response = request_obj.next(next_page)
                    else:
                        break
                else:
                    break

            residues_list_ext_ids = []
            for residue in residue_list:
                ean13 = residue.get('ean13')
                eanOther = residue.get('eanOther')
                if eanOther and self.conf.USE_EAN_OTHER:
                    ean13_list = eanOther
                else:
                    ean13_list = [ean13]
                gtin = residue.get('gtin')
                series = residue.get('series')
                warehouseExtId = residue.get('warehouseExtId')
                quantity = residue.get('quantity')
                expirationDate = residue.get('expirationDate')
                ext_id = residue.get('extId')
                skuExtId = residue.get('skuExtId')

                residues_db = Residue.objects.filter(
                    ean13__in=ean13_list,
                    warehouse_ext_id=branch.inn,
                    series=series,
                    pk=ext_id,
                    sended=True
                )

                if residues_db.exists():
                    residues_list_ext_ids.append(ext_id)
                    for residue_db in residues_db:
                        if quantity != residue_db.quantity:

                            if residue_db.quantity > quantity:
                                quantity_discrepancies = residue_db.quantity - quantity
                            else:
                                quantity_discrepancies = quantity - residue_db.quantity

                            ReconciliationResidue.objects.create(
                                gtin=residue_db.gtin,
                                series=residue_db.series,
                                ean13=residue_db.ean13,
                                warehouse_ext_id=residue_db.warehouse_ext_id,
                                quantity=residue_db.quantity,
                                quantity_in_pz=quantity,
                                expiration_date=residue_db.expiration_date,
                                ext_id=residue_db.ext_id,
                                nomenclature=residue_db.nomenclature,
                                not_equal_quantity=True,
                                quantity_discrepancies=quantity_discrepancies,
                                comment=f'Расхождение остатка.\neanOther={eanOther}',
                                uid_reconciliation=uid_reconciliation
                            )

                            is_error = True

                else:
                    if quantity:

                        ReconciliationResidue.objects.create(
                            gtin=gtin,
                            series=series,
                            ean13=ean13,
                            warehouse_ext_id=warehouseExtId,
                            quantity=0,
                            quantity_in_pz=quantity,
                            expiration_date=expirationDate,
                            ext_id=ext_id,
                            nomenclature=skuExtId,
                            not_in_residue=True,
                            quantity_discrepancies=quantity,
                            comment=f'Не существует остаток в нашей БД eanOther={eanOther}',
                            uid_reconciliation=uid_reconciliation
                        )

                        is_error = True

            residues_db = Residue.objects.exclude(
                pk__in=residues_list_ext_ids
            ).filter(
                sended=True,
                warehouse_ext_id=branch.inn
            )
            for residue_db in residues_db:

                ReconciliationResidue.objects.create(
                    gtin=residue_db.gtin,
                    series=residue_db.series,
                    ean13=residue_db.ean13,
                    warehouse_ext_id=residue_db.warehouse_ext_id,
                    quantity=residue_db.quantity,
                    quantity_in_pz=0,
                    expiration_date=residue_db.expiration_date,
                    ext_id=residue_db.ext_id,
                    nomenclature=residue_db.nomenclature,
                    not_in_pz=True,
                    quantity_discrepancies=residue_db.quantity,
                    comment='Нет в фармзаказе.',
                    uid_reconciliation=uid_reconciliation
                )

                is_error = True

        if is_error:
            msg = f'Обнаружены расходения.\nДоступ по ссылке:\n' \
                  f'{self.conf.RESIDUE_URL_FOR_TG_BOT}{uid_reconciliation}'
            bot = PharmZakazTelegramBot()
            bot.send_msg(msg=msg)
