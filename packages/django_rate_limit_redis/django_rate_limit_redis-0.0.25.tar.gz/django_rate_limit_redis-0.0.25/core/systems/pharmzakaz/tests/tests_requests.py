from unittest import mock

from rest_framework import status

from django.conf import settings
from django.test import TestCase

from core.systems.pharmzakaz.requests import BonusesRequest
from core.systems.pharmzakaz.requests import InvoicesRequest
from core.systems.pharmzakaz.requests import LegalEntitiesRequest
from core.systems.pharmzakaz.requests import OrdersRequest
from core.systems.pharmzakaz.requests import SKURequest
from core.systems.pharmzakaz.requests import StoresRequest
from core.systems.pharmzakaz.requests import WarehousesRequest
from core.systems.pharmzakaz.tests.mock_requests import MockRequests
from core.systems.pharmzakaz.tests.tests_requests_data import BonusesRequestTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import InvoicesRequestTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import LegalEntitiesTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import OrdersRequestTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import SKURequestTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import StoresRequestTestCaseData
from core.systems.pharmzakaz.tests.tests_requests_data import WarehousesRequestTestCaseData

endpoint = settings.PHARMZAKAZENDPOINT   # "https://demo.pharm-zakaz.ru/api/distributor/v1/"


class StoresRequestTestCase(TestCase, StoresRequestTestCaseData, MockRequests):
    url = endpoint + "stores/"

    def setUp(self):
        self.stores_request = StoresRequest()
        self.storeInfoId = 273581
        self.warehouseId = 102

    def test_stores_list(self):
        self.response_get = self.list_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.stores_request.stores_list(warehouseId=self.warehouseId)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_stores_create(self):
        self.data_post = self.create_data_post
        self.response_post = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.post', side_effect=self.mocked_requests_post):
            response = self.stores_request.stores_create(**self.data_post)
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_stores_read(self):
        self.url += f"{self.storeInfoId}/"
        self.response_get = self.read_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.stores_request.stores_read(self.storeInfoId)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_stores_partial_update(self):
        self.url += f"{self.storeInfoId}/"
        self.data_post = self.partial_update_data_patch
        self.response_patch = self.partial_update_response_patch
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            response = self.stores_request.stores_partial_update(self.storeInfoId, **self.data_post)
            self.assertEqual(status.HTTP_200_OK, response.status_code)


class SKURequestTestCase(TestCase, SKURequestTestCaseData, MockRequests):
    url = endpoint + "sku/"

    def setUp(self):
        self.SKU_request = SKURequest()
        self.storeInfoId = 273581
        self.ean13 = "4604060081014"
        self.extSkuId = "04492"
        self.warehouseId = 102

    def test_sku_list(self):
        self.response_get = self.list_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.SKU_request.sku_list()
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_sku_update_sku_list(self):
        self.url += "update/"
        self.data_post = self.create_data_post
        self.response_post = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.post', side_effect=self.mocked_requests_post):
            response = self.SKU_request.sku_update_sku_list(sku_list=self.data_post)
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_sku_read(self):
        self.url += f"{self.ean13}/"
        self.response_get = self.read_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.SKU_request.sku_read(self.ean13)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_sku_partial_update(self):
        self.url += f"{self.ean13}/"
        self.data_post = self.patch_data
        self.response_patch = self.patch_response
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            response = self.SKU_request.sku_partial_update(self.ean13, *self.patch_data.values())
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_sku_residues_list(self):
        self.url += f"{self.ean13}/residues/"
        self.response_get = self.sku_residues_list
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.SKU_request.sku_residues_list(self.ean13, self.warehouseId)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_sku_residues_update_residues_list(self):
        self.url += f"{self.ean13}/residues/update/"
        self.data_post = self.sku_residues_update_residues_list_data_post
        self.response_post = self.sku_residues_update_residues_list_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.post', side_effect=self.mocked_requests_post):
            response = self.SKU_request.sku_residues_update_residues_list(self.ean13, sku_residues_list=self.data_post)
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class WarehousesRequestTestCase(TestCase, WarehousesRequestTestCaseData, MockRequests):
    url = endpoint + "warehouses/"

    def setUp(self):
        self.warehouses_request = WarehousesRequest()
        self.warehouseId = 102

    def test_warehouses_list(self):
        self.response_get = self.list_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.warehouses_request.warehouses_list()
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_warehouses_create(self):
        self.data_post = self.create_data_post
        self.response_post = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.post', side_effect=self.mocked_requests_post):
            response = self.warehouses_request.warehouses_create(*self.data_post.values())
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_warehouses_read(self):
        self.url += f"{self.warehouseId}/"
        self.response_get = self.read_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.warehouses_request.warehouses_read(self.warehouseId)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_warehouses_partial_update(self):
        self.url += f"{self.warehouseId}/"
        self.data_post = self.partial_update_data_patch
        self.response_patch = self.partial_update_response_patch
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            response = self.warehouses_request.warehouses_partial_update(self.warehouseId, *self.data_post.values())
            self.assertEqual(status.HTTP_200_OK, response.status_code)


class OrdersRequestTestCase(TestCase, OrdersRequestTestCaseData, MockRequests):
    url = endpoint + "orders/"

    def setUp(self):
        self.orders_request = OrdersRequest()
        self.warehouseId = 102
        self.orderId = 1

    def test_orders_list(self):
        self.response_get = self.list_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.orders_request.orders_list(warehouseId=self.warehouseId)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_orders_read(self):
        self.url += f"{self.orderId}/"
        self.response_get = self.read_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.orders_request.orders_read(self.orderId)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_orders_partial_update(self):
        self.url += f"{self.orderId}/"
        self.data_post = self.partial_update_data_patch
        self.response_patch = self.partial_update_response_patch
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            response = self.orders_request.orders_partial_update(self.orderId, **self.data_post)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_orders_returns_update(self):
        self.url += f"{self.orderId}/returns/"
        self.data_post = self.partial_returns_update_data_patch
        self.response_patch = self.partial_returns_update_response_patch
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            response = self.orders_request.orders_returns_update(self.orderId, **self.data_post)
            self.assertEqual(status.HTTP_200_OK, response.status_code)


class InvoicesRequestTestCase(TestCase, InvoicesRequestTestCaseData, MockRequests):
    url = endpoint + "invoices/"

    def setUp(self):
        self.invoices_request = InvoicesRequest()
        self.warehouseId = 102
        self.invoiceId = 1

    def test_invoices_list(self):
        self.response_get = self.list_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.invoices_request.invoices_list(warehouseId=self.warehouseId)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_invoices_create(self):
        self.data_post = self.create_data_post
        self.response_post = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.post', side_effect=self.mocked_requests_post):
            response = self.invoices_request.invoices_create(**self.data_post)
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_invoices_read(self):
        self.url += f"{self.invoiceId}/"
        self.response_get = self.read_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.invoices_request.invoices_read(self.invoiceId)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_invoices_partial_update(self):
        self.url += f"{self.invoiceId}/"
        self.data_post = self.partial_returns_update_data_patch
        self.response_patch = self.partial_returns_update_response_patch
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            response = self.invoices_request.invoices_partial_update(self.invoiceId, **self.data_post)
            self.assertEqual(status.HTTP_200_OK, response.status_code)


class BonusesRequestTestCase(TestCase, BonusesRequestTestCaseData, MockRequests):
    url = endpoint + "bonuses/"

    def setUp(self):
        self.bonuses_request = BonusesRequest()
        self.bonusId = 3
        self.bonusPaymentStatus = "3"
        self.statusDate = "2022-01-25T08:18:56.084Z"

    def test_bonuses_accurals_list(self):
        self.url += 'accurals/'
        self.response_get = self.accurals_list_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.bonuses_request.bonuses_accurals_list()
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_bonuses_payments_list(self):
        self.url += 'payments/'
        self.response_get = self.payments_list_response_get
        self.params = self.payments_list_params_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.bonuses_request.bonuses_payments_list(**self.params)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_bonuses_payments_create(self):
        self.url += f"payments/{self.bonusId}/"
        self.data_post = self.create_data_post
        self.response_patch = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.put', side_effect=self.mocked_requests_patch):
            response = self.bonuses_request.bonuses_payments_create(self.bonusId, self.bonusPaymentStatus,
                                                                    self.statusDate, comment="string",
                                                                    paymentOrder="string", extId=0)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_bonuses_payments_update(self):
        self.url += f"payments/{self.bonusId}/"
        self.data_post = self.create_data_post
        self.response_patch = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            response = self.bonuses_request.bonuses_payments_update(self.bonusId, self.bonusPaymentStatus,
                                                                    self.statusDate, comment="string",
                                                                    paymentOrder="string", extId=0)
            self.assertEqual(status.HTTP_200_OK, response.status_code)


class LegalEntitiesRequestTestCase(TestCase, LegalEntitiesTestCaseData, MockRequests):
    url = endpoint + "legal-entities/"

    def setUp(self):
        self.legal_entities_request = LegalEntitiesRequest()
        self.entity_id = 1

    def test_legal_entities_list(self):
        self.response_get = self.legal_entities_list
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.legal_entities_request.legal_entities_list()
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_legal_entities_requests_list(self):
        self.url += "requests/"
        self.response_get = self.legal_entities_requests_list
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.legal_entities_request.legal_entities_requests_list()
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_legal_entities_create(self):
        self.data_post = self.create_data_post
        self.response_post = self.create_response_post
        with mock.patch('core.systems.pharmzakaz.requests.requests.post', side_effect=self.mocked_requests_post):
            response = self.legal_entities_request.legal_entities_create(**self.data_post)
            self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_legal_entities_read(self):
        self.url += f"{self.entity_id}/"
        self.response_get = self.read_response_get
        with mock.patch('core.systems.pharmzakaz.requests.requests.get', side_effect=self.mocked_requests_get):
            response = self.legal_entities_request.legal_entities_read(self.entity_id)
            self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_legal_entities_partial_update(self):
        self.url += f"{self.entity_id}/"
        self.data_post = self.partial_update_data_patch
        self.response_patch = self.partial_update_response_patch
        with mock.patch('core.systems.pharmzakaz.requests.requests.patch', side_effect=self.mocked_requests_patch):
            response = self.legal_entities_request.legal_entities_partial_update(self.entity_id, **self.data_post)
            self.assertEqual(status.HTTP_200_OK, response.status_code)
