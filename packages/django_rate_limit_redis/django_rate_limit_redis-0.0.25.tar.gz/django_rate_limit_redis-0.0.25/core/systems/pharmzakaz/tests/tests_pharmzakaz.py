import datetime
from unittest import mock

from rest_framework import status

from django.conf import settings
from django.test import TestCase

from core.consts import LEGAL_ENTITY_ACTUAL
from core.consts import LEGAL_ENTITY_NOT_ACTUAL
from core.models import Branch
from core.models import Invoice
from core.models import KafkaMsg
from core.models import LegalEntity
from core.models import LegalEntityOnboarded
from core.models import Order
from core.models import Residue
from core.models import Store
from core.systems.pharmzakaz.pharmzakaz import PharmZakazSystem
from core.systems.pharmzakaz.tests.mock_requests import MockRequests
from core.systems.pharmzakaz.tests.mock_requests import MockResponse
from core.systems.pharmzakaz.tests.tests_requests_data import InvoicesRequestTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import LegalEntitiesTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import OrdersRequestTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import ResudieTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import StoresRequestTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import WarehousesRequestTestCaseData

endpoint = settings.PHARMZAKAZENDPOINT


class StoresRequestTestCase(TestCase, StoresRequestTestCaseData, MockRequests):
    fixtures = ['Store', 'test_Branch']
    url = endpoint + "stores/"

    def setUp(self):
        self.pz_systems = PharmZakazSystem

    def test_create_store(self):
        store_pk = 40
        self.data_post = self.create_data_post
        self.response_post = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.post', side_effect=self.mocked_requests_post):
            qs = Store.objects.filter(pk=store_pk)
            self.pz_systems().create_store(qs=qs)
            obj = Store.objects.get(pk=store_pk)
            self.assertEqual(obj.store_info_id, 273581)
            self.assertEqual(obj.sended, True)

    def test_update_one_store(self):
        store_pk = 40
        self.url += "273581/"
        self.data_post = self.create_data_post
        self.response_post = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_post):
            Store.objects.filter(pk=store_pk).update(store_info_id=273581, sended=False)
            store = Store.objects.get(pk=store_pk)
            self.pz_systems().update_one_store(store=store)
            store.refresh_from_db()
            self.assertEqual(store.store_info_id, 273581)
            self.assertEqual(store.sended, True)

    def test_read_list_stores(self):
        store_info_id_list = [273691, 274105, 274047]
        self.response_get = self.get_read_list_stores
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            self.pz_systems().read_list_stores()
            for store_info_id in store_info_id_list:
                store = Store.objects.get(store_info_id=store_info_id)
                self.assertEqual(store.store_info_id, store_info_id)
                self.assertEqual(store.sended, True)

    def test_read_one_store(self):
        store_info_id = 274047
        self.url += f"{store_info_id}/"
        self.response_get = self.get_read_list_stores.get('results')[2]
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            self.pz_systems().read_one_store(store_info_id)
            store = Store.objects.get(store_info_id=store_info_id)
            self.assertEqual(store.store_info_id, store_info_id)
            self.assertEqual(store.sended, True)


class ResidueTestCase(TestCase, ResudieTestCaseData, MockRequests):
    fixtures = ['test_Branch', 'Residue', 'ResidueHistory', 'Settings', 'RateLimit']
    url = ''

    def setUp(self):
        self.pz_systems = PharmZakazSystem

    def mocked_requests_post_residue(self, *args, **kwargs):
        import json
        ean13 = str(json.loads(kwargs.get("data"))[0].get('EAN13'))
        self.url = f"{endpoint}sku/{ean13}/residues/update/"
        self.response_post = self.create_response_post.get(ean13)
        self.data_post = self.create_data_post.get(ean13)

        return super().mocked_requests_post(*args, **kwargs)

    def test_update_all_residues_batch(self):
        with mock.patch(
                'core.systems.pharmzakaz.requests.requests.post',
                side_effect=self.mocked_requests_post_residue
        ):
            self.pz_systems().update_all_residues_batch()
            residue = Residue.objects.get(ean13="4601969000580")
            self.assertEqual(residue.sended, True)
            residue = Residue.objects.get(ean13="4601969000511")
            self.assertEqual(residue.sended, True)

    def test_get_diff_residues(self):
        qs = self.pz_systems().get_diff_residues(3255510243)
        self.assertEqual(list(qs.values_list()), self.diff_residues)


class OrdersTestCase(TestCase, OrdersRequestTestCaseData, MockRequests):
    fixtures = ['test_Branch', 'Orders', 'Positions', 'Nomenclature']
    params = ''
    key_field = None
    url = ''

    def setUp(self):
        self.pz_systems = PharmZakazSystem

    def mocked_requests_get_with_params(self, *args, **kwargs):
        self.params = kwargs.get("params")
        return super().mocked_requests_get(*args, **kwargs)

    def test_get_list_orders(self):
        self.url = f'{endpoint}orders/'
        self.response_get = self.get_list_orders
        with mock.patch(
                'core.systems.pharmzakaz.requests.requests.get',
                side_effect=self.mocked_requests_get_with_params
        ):

            qs = Branch.objects.filter(warehouse_id=130)
            self.pz_systems().get_new_list_orders(qs=qs)
            self.assertEqual(self.params, self.orders_request_params)
            order = Order.objects.get(order_id=255592)
            self.assertEqual(order.status, 'transmitted')

    def test_get_last_order_with_branch(self):
        branch = Branch.objects.get(warehouse_id=102)
        created_date = self.pz_systems().get_last_order_with_branch(branch)
        self.assertEqual(created_date, datetime.date(2022, 2, 18))

    def test_order_update(self):
        order_id = 255453
        self.key_field = 'EAN13'
        self.url = f'{endpoint}orders/{order_id}/'
        self.data_post = self.order_update_data_patch
        self.response_patch = self.order_update_response_patch
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            self.pz_systems().order_update(order_id, order_status='transmitted')
            order = Order.objects.get(order_id=order_id)
            self.assertEqual(order.status, 'transmitted')

    def test_save_msg_order_after_download(self):
        qs = Order.objects.filter(order_id=255454)
        order_ids = list(qs.values_list('order_id', flat=True))
        self.pz_systems().save_msg_order_after_download(order_ids)
        msg = KafkaMsg.objects.all().first().msg
        self.assertEqual(
            msg.get("#value")[1].get("#value"),
            self.kafka_msg.get("#value")[1].get("#value")
        )


class InvoiceTestCase(TestCase, InvoicesRequestTestCaseData, MockRequests):
    fixtures = ['test_Branch', 'Invoices']
    params = ''
    key_field = None
    url = ''

    def setUp(self):
        self.pz_systems = PharmZakazSystem

    # def mocked_requests_patch_v1(self, *args, **kwargs):
    #     print(args, kwargs)
    #     return super().mocked_requests_patch(*args, **kwargs)

    def test_create_invoice(self):
        invoice_num = 'НСКР0115309'
        self.url = f'{endpoint}invoices/'
        self.data_post = self.test_create_invoice_data_post
        self.response_post = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.post', side_effect=self.mocked_requests_post):
            qs = Invoice.objects.filter(invoice_num=invoice_num)
            self.pz_systems().create_invoice(qs=qs)

    def test_get_invoice(self):
        invoice_id = 200
        self.url = f'{endpoint}invoices/{invoice_id}/'
        self.response_get = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            result = self.pz_systems().get_invoice(invoice_id=invoice_id)
            self.assertTrue(result)

    def test_list_invoice(self):
        invoice_ids = [69, 68, 70, 71, 72, 73, 74, 75, 76, 80, 81]
        self.url = f'{endpoint}invoices/'
        self.response_get = self.test_list_invoice_response
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            qs = Branch.objects.filter(warehouse_id=130)
            self.pz_systems().list_invoice(qs=qs)
            for invoice_id in invoice_ids:
                qs = Invoice.objects.filter(invoice_id=invoice_id)
                self.assertTrue(qs.exists())

    def test_update_invoice(self):
        invoice_num = 'БРН0012346'
        invoice_id = 65
        Invoice.objects.filter(invoice_num=invoice_num).update(sended=False)
        self.url = f'{endpoint}invoices/{invoice_id}/'
        self.data_post = self.test_update_invoice_data_pathc
        self.response_patch = self.test_update_invoice_response_patch
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            qs = Invoice.objects.filter(invoice_num=invoice_num)
            self.pz_systems().update_invoice(qs=qs)
            invoice = Invoice.objects.filter(invoice_num=invoice_num).first()
            self.assertTrue(invoice.sended)


class WarehousesTestCase(TestCase, WarehousesRequestTestCaseData, MockRequests):
    fixtures = ['test_Branch']
    url = endpoint + "warehouses/"

    def setUp(self):
        self.pz_systems = PharmZakazSystem

    def test_send_warehouses(self):
        Branch.objects.filter(pk=4).update(warehouse_id=None, sended=False, sended_at=None)
        self.data_post = self.send_warehouses_data_post
        self.response_post = self.send_warehouses_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.post', side_effect=self.mocked_requests_post):
            qs = Branch.objects.filter(pk=4)
            self.pz_systems().send_warehouses(qs)
            branch = Branch.objects.get(pk=4)
            self.assertEqual(branch.sended, True)

    def test_update_warehouses(self):
        Branch.objects.filter(pk=4).update(sended=False, sended_at=None, warehouse_id=130)
        self.url += "130/"
        self.data_post = self.send_warehouses_data_post
        self.response_patch = self.send_warehouses_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            qs = Branch.objects.filter(pk=4)
            self.pz_systems().update_warehouses(qs)
            branch = Branch.objects.get(pk=4)
            self.assertEqual(branch.sended, True)


class LegalEntityRequestTestCase(TestCase, LegalEntitiesTestCaseData, MockRequests):
    fixtures = ['Branch.json']
    url = endpoint + "legal-entities/requests/"

    def setUp(self):
        self.pz_systems = PharmZakazSystem

    def test_get_and_create_request(self):
        self.response_get = self.legal_entities_requests_list

        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            # эмуляция первого запроса
            self.pz_systems().get_new_legal_entities()
            obj = LegalEntity.objects.get(pharm_zakaz_id=43522)
            self.assertEqual(LegalEntity.objects.all().count(), 1)
            self.assertEqual(obj.sended_to_1c, False)
            self.assertEqual(obj.status, LEGAL_ENTITY_ACTUAL)

            # эмуляция второго запроса
            self.pz_systems().get_new_legal_entities()
            self.assertEqual(LegalEntity.objects.all().count(), 1)

        # Отправляем в кафка
        self.pz_systems().send_legal_entities_to_1C()
        self.assertEqual(KafkaMsg.objects.all().count(), 14)

        # эмуляция изменения статуса
        self.response_get = self.legal_entities_requests_list_with_changed_status
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            self.pz_systems().get_new_legal_entities()
            self.assertEqual(LegalEntity.objects.all().count(), 1)
            obj = LegalEntity.objects.get(pharm_zakaz_id=43522)
            self.assertEqual(obj.status, LEGAL_ENTITY_NOT_ACTUAL)

        # проверяю как будет работать генерация сообщения в кафка
        self.pz_systems().send_legal_entities_to_1C()
        self.assertEqual(KafkaMsg.objects.all().count(), 28)
        obj.refresh_from_db()
        self.assertEqual(obj.sended_to_1c, True)


class LegalEntityOnboardedTestCase(TestCase, LegalEntitiesTestCaseData):
    fixtures = ['LegalEntityOnboarded', ]

    def setUp(self):
        self.pz_systems = PharmZakazSystem()

    def mocked_requests_post(self, *args, **kwargs):
        return MockResponse(self.create_response_post, status.HTTP_201_CREATED)

    def mocked_requests_patch(self, *args, **kwargs):
        return MockResponse(self.partial_update_response_patch, status.HTTP_200_OK)

    def test_create_legal_entity_onboarded(self):
        with mock.patch('core.systems.pharmzakaz.requests.requests.post', side_effect=self.mocked_requests_post):
            with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
                self.pz_systems.send_onboarded_legal_entities()
                leo_need_to_be_created = LegalEntityOnboarded.objects.get(inn="1234235")
                self.assertEqual(leo_need_to_be_created.sended_to_pz, True)
                self.assertNotEqual(leo_need_to_be_created.sended_to_pz_at, None)
                self.assertEqual(leo_need_to_be_created.pharm_zakaz_id, 0)

                leo_need_to_be_updated = LegalEntityOnboarded.objects.get(inn="9242235")
                self.assertEqual(leo_need_to_be_updated.sended_to_pz, True)
                self.assertNotEqual(leo_need_to_be_updated.sended_to_pz_at, None)
                self.assertEqual(leo_need_to_be_updated.pharm_zakaz_id, 414)
