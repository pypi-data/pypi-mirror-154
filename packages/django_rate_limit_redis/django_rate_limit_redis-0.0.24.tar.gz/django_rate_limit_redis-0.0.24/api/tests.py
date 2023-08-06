from decimal import Decimal

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from django.urls import reverse

from core.models import BonusPayment
from core.models import Order
from core.models import Position
from core.models import Residue
from core.models import Store
from core.tests.factories import BonusPaymentFactory
from core.tests.factories import OrderFactory
from core.tests.factories import ResidueFactory
from core.tests.factories import StoreFactory


class StoreTestCase(APITestCase):
    fixtures = ['authtoken_token', 'users_appuser', ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.key_list_from_model = [f for f in Store.alias_fields.keys()]
        cls.BATCH_SIZE = 100

    def test_list(self):
        StoreFactory.create_batch(size=self.BATCH_SIZE)
        self.client.credentials(HTTP_AUTHORIZATION='Token 70c271a03e413d03c84d3364b5c65f3fdb7bc8bd')
        response = self.client.get(reverse('store-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.BATCH_SIZE)

        # проверка наличия полей
        key_list_from_response = list(response.data[0].keys())
        self.assertEqual(self.key_list_from_model, key_list_from_response)

        # проверка значения полей
        store_from_db = Store.objects.get(pos_ext_id=response.data[0]['posExtId'])
        self.assertEqual(response.data[0]['fiasId'], store_from_db.fias_id)

    def test_detail(self):
        store = StoreFactory()
        stores_detail_url = reverse('store-detail', args=(store.pos_ext_id,))
        self.client.credentials(HTTP_AUTHORIZATION='Token 70c271a03e413d03c84d3364b5c65f3fdb7bc8bd')
        response = self.client.get(stores_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка наличия полей
        key_list_from_response = list(response.data.keys())
        self.assertEqual(self.key_list_from_model, key_list_from_response)

        # проверка значения полей
        self.assertEqual(response.data['fiasCode'], store.fias_code)


class OrderTestCase(APITestCase):
    fixtures = ['authtoken_token', 'users_appuser', ]

    @classmethod
    def setUpClass(cls):  # TODO вынести в отдельный класс, от которого наследуемся
        super().setUpClass()
        cls.client = APIClient()
        cls.key_list_from_model = [f for f in Order.alias_fields.keys()]
        exclude_field = ['warehouseExtId', 'positionId']
        cls.position_model_fields = [f for f in Position.alias_fields.keys() if f not in exclude_field]
        cls.BATCH_SIZE = 100

    def test_order_list(self):
        OrderFactory.create_batch(size=self.BATCH_SIZE)
        self.client.credentials(HTTP_AUTHORIZATION='Token 70c271a03e413d03c84d3364b5c65f3fdb7bc8bd')
        response = self.client.get(reverse('order-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.BATCH_SIZE)

        # проверка наличия полей у Order в ответе
        key_list_from_response = list(response.data[0].keys())
        self.assertCountEqual(self.key_list_from_model, key_list_from_response)

        # проверка значения полей у Order в ответе
        order_from_db = Order.objects.get(order_id=response.data[0]['orderId'])
        self.assertEqual(Decimal(response.data[0]['totalSum']), order_from_db.total_sum)

        # проверка корректного количества Positions в ответе
        self.assertEqual(len(response.data[0]['positions']), order_from_db.positions.count())

        # проверка наличия полей у Position в ответе
        position_fields_from_response = list(response.data[0]['positions'][0].keys())
        self.assertCountEqual(self.position_model_fields, position_fields_from_response)

        # проверка значения полей у Position в ответе
        position_from_db = Position.objects.get(ext_id=response.data[0]['positions'][0]['extId'])
        self.assertEqual(response.data[0]['positions'][0]['GTIN'], position_from_db.gtin)

    def test_detail(self):
        order = OrderFactory()
        order_detail_url = reverse('order-detail', args=(order.order_id,))
        self.client.credentials(HTTP_AUTHORIZATION='Token 70c271a03e413d03c84d3364b5c65f3fdb7bc8bd')
        response = self.client.get(order_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка наличия полей у Order в ответе
        key_list_from_response = list(response.data.keys())
        self.assertCountEqual(self.key_list_from_model, key_list_from_response)

        # проверка значения полей у Order в ответе
        self.assertEqual(Decimal(response.data['totalSum']), order.total_sum)

        # проверка наличия полей у Position в ответе
        position_fields_from_response = list(response.data['positions'][0].keys())
        self.assertCountEqual(self.position_model_fields, position_fields_from_response)

        # проверка значения полей у Position в ответе
        position_from_db = Position.objects.get(ext_id=response.data['positions'][0]['extId'])
        self.assertEqual(response.data['positions'][0]['GTIN'], position_from_db.gtin)


class ResidueTestCase(APITestCase):
    fixtures = ['authtoken_token', 'users_appuser', 'RateLimit']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.key_list_from_model = [f for f in Residue.alias_fields.keys()]
        cls.BATCH_SIZE = 100

    def test_list(self):
        ResidueFactory.create_batch(size=self.BATCH_SIZE)
        residue = Residue.objects.all().first()
        self.client.credentials(HTTP_AUTHORIZATION='Token 70c271a03e413d03c84d3364b5c65f3fdb7bc8bd')
        response = self.client.get(reverse('residue-list', args=(residue.ean13,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.BATCH_SIZE)

        self.assertNotEqual(len(response.data['next']), '')
        self.assertEqual(response.data['previous'], None)

        # проверка наличия полей
        key_list_from_response = list(response.data['results'][0].keys())
        self.assertEqual(self.key_list_from_model.sort(), key_list_from_response.sort())


class BonusPaymentTestCase(APITestCase):
    fixtures = ['authtoken_token', 'users_appuser', 'RateLimit']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.key_list_from_model = [f for f in BonusPayment.alias_fields.keys()]
        cls.BATCH_SIZE = 100

    def test_list(self):
        BonusPaymentFactory.create_batch(size=self.BATCH_SIZE)
        self.client.credentials(HTTP_AUTHORIZATION='Token 70c271a03e413d03c84d3364b5c65f3fdb7bc8bd')
        response = self.client.get(reverse('bonus_payment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.BATCH_SIZE)

        self.assertNotEqual(len(response.data['next']), '')
        self.assertEqual(response.data['previous'], None)

        # проверка наличия полей
        key_list_from_response = list(response.data['results'][0].keys())
        self.assertEqual(self.key_list_from_model, key_list_from_response)
