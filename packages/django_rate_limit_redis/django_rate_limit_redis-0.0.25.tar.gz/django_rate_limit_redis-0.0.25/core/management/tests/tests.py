import json
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from core.consts import ORDER_STATUSES_ONE_C
from core.models import Invoice
from core.models import Order
from core.models import OrderStatusMap
from core.models import Residue


class KafkaConsumerMsg:
    TopicPartition = None

    def __init__(self, msg):
        self.msg = [msg]

    def __iter__(self):
        return iter(self.msg)

    def __next__(self):
        return next(self.msg)

    def assign(self, *args, **kwargs):
        self.TopicPartition = args[0]


class BaseTestCase(TestCase):
    msg_consumer = None

    def call_command(self, topic: str):
        args = [topic, ]
        opts = {}
        call_command('start_consume', *args, **opts)

    def get_kafka_msg(self, fix_name):
        with open(f'/app/core/fixtures/kafka/{fix_name}.json') as f:
            self.fixture = json.load(f)
            msg = json.dumps(self.fixture).encode('utf-8')
            return msg

    def return_kafka_msg(self, *args, **kwargs):
        self.msg_consumer = KafkaConsumerMsg(self.msg)
        return self.msg_consumer


class KafkaMsg:
    offset = 10
    partition = 0

    def __init__(self, value, topic):
        self.value = value
        self.topic = topic


class OrdersTopicConsumerTestCase(BaseTestCase):
    fixtures = ("OrderDataHandler.json", "DataHandlersMap.json")
    status_map = dict((y, x) for x, y in ORDER_STATUSES_ONE_C)

    def test_orders_topic_consume(self):
        topic = 'Orders_topic_message'
        kafka_msg = self.get_kafka_msg(topic)
        self.msg = KafkaMsg(kafka_msg, topic)
        with patch('core.management.commands.start_consume.KafkaConsumerClass', side_effect=self.return_kafka_msg):
            self.call_command('orderstopic')
        status_pz = self.status_map.get(self.fixture.get("status"))
        status = OrderStatusMap.objects.get(status_one_c=status_pz).status_pharm_zakaz

        obj = Order.objects.get(order_id=2)

        self.assertEqual(obj.status, status)
        self.assertEqual(obj.warehouse_ext_id, self.fixture.get("inn"))
        self.assertEqual(obj.total_sum, self.fixture.get("checksum_total"))
        self.assertEqual(obj.vat_sum, self.fixture.get("total_VAT"))
        self.assertEqual(obj.document_number, self.fixture["document_number"])


class InstocktopicConsumerTestCase(BaseTestCase):
    fixtures = ("Nomenclature.json", "DataHandlersMap.json")

    def test_instocks_topic_consume(self):
        topic = 'Instock_topic_message'
        kafka_msg = self.get_kafka_msg(topic)
        self.msg = KafkaMsg(kafka_msg, topic)
        with patch('core.management.commands.start_consume.KafkaConsumerClass', side_effect=self.return_kafka_msg):
            self.call_command('FarmZakaz_Stock_test')

        obj = Residue.objects.first()

        self.assertEqual(obj.nomenclature, self.fixture.get("goodscode"))
        self.assertEqual(obj.quantity, self.fixture.get("quantity"))
        self.assertEqual(obj.warehouse_ext_id, self.fixture.get("inn"))
        self.assertEqual(obj.series, self.fixture.get("series_code"))


class SalesTopicV2ConsumerTestCase(BaseTestCase):
    fixtures = ("DataHandlersMap.json", )

    def test_sales_topic_consume(self):
        topic = 'Salestopicv2_message'
        kafka_msg = self.get_kafka_msg(topic)
        self.msg = KafkaMsg(kafka_msg, topic)
        with patch('core.management.commands.start_consume.KafkaConsumerClass', side_effect=self.return_kafka_msg):
            self.call_command('salestopicV2')

        obj = Invoice.objects.get(invoice_num="ЯРС00159526")

        self.assertEqual(obj.invoice_num, self.fixture.get("document_number"))
        self.assertEqual(obj.store_ext_id, self.fixture.get("address_code"))
        self.assertEqual(obj.delivered_quantity, self.fixture.get("quantity"))
        self.assertEqual(obj.sku_ext_id, self.fixture.get("goodscode"))
        self.assertEqual(float(obj.delivered_sum), self.fixture.get("checksum_total"))


class ConsumerMapingTestCase(BaseTestCase):
    fixtures = ("Nomenclature.json", "DataHandlersMap.json")

    def test_maping_consumer(self):
        topic = 'Instock_topic_message'
        data_handler = 'InStockTopic'
        target_topic = 'FarmZakaz_Stock_test'
        kafka_msg = self.get_kafka_msg(topic)
        self.msg = KafkaMsg(kafka_msg, topic)
        with patch('core.management.commands.start_consume.KafkaConsumerClass', side_effect=self.return_kafka_msg):
            self.call_command(data_handler)
            self.assertEqual(target_topic, self.msg_consumer.TopicPartition[0][0])
