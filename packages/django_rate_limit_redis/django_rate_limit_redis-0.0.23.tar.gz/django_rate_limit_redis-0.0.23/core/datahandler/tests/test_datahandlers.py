from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from core.datahandler import DataHandlerFactory
from core.datahandler.tests.test_datahandlers_data import INSTOCKTOPIC_DATA
from core.datahandler.tests.test_datahandlers_data import LEGAL_ENTITY_ONBOARDED
from core.datahandler.tests.test_datahandlers_data import NOMENCLATURE
from core.datahandler.tests.test_datahandlers_data import ORDER_TOPIC_DATA
from core.datahandler.tests.test_datahandlers_data import SALES_TOPIC_V2_DATA
from core.datahandler.tests.test_datahandlers_data import SALES_TOPIC_V2_UPDATE_DATA
from core.models import Invoice
from core.models import LegalEntityOnboarded
from core.models import Nomenclature
from core.models import Order
from core.models import Residue
from core.models import ResidueHistory


class BaseTestCase:
    def get_date(self, date):  # преобразует строку-дату из входящего в дату
        return timezone.localtime(datetime.strptime(date, "%d.%m.%Y %H:%M:%S").astimezone())


class OrderTopicDataHandlerTestCase(TestCase, BaseTestCase):
    fixtures = ("OrderDataHandler.json", "DataHandlersMap.json")  # ЭТО ТО, ЧТО БУДЕТ ПРЕДЗАГРУЖЕНО ПРЕД ТЕСТОМ

    def setUp(self):
        self.data = ORDER_TOPIC_DATA  # берётся из файла test_datahandlers_data. ЭТО ТО ЧТО ПРИДЁТ НА ВХОД

    def test_save_data(self):
        datahandler = DataHandlerFactory.get_handler(self.data, "orderstopic")
        datahandler.save_data()
        obj = Order.objects.get(order_id=1)
        self.assertEqual(obj.document_number, self.data["document_number"])


class SalesTopicV2TopicDataHandlerTestCase(TestCase, BaseTestCase):
    fixtures = ("DataHandlersMap.json", )

    def setUp(self):
        self.data = SALES_TOPIC_V2_DATA
        self.update_data = SALES_TOPIC_V2_UPDATE_DATA

    def save_data(self):
        datahandler = DataHandlerFactory.get_handler(self.data, "salestopicV2")
        datahandler.save_data()

    def test_save_data(self):
        self.save_data()
        obj = Invoice.objects.get(invoice_num="МСК00656753")
        self.assertEqual(obj.invoice_num, self.data["document_number"])
        self.assertEqual(obj.created, self.get_date(self.data["datevalue"]))

    def test_update_data(self):
        self.save_data()
        datahandler = DataHandlerFactory.get_handler(self.update_data, "salestopicV2")
        datahandler.save_data()
        obj = Invoice.objects.get(invoice_num="МСК00656753")
        len_qs = Invoice.objects.filter(invoice_num="МСК00656753").count()
        self.assertEqual(obj.invoice_num, self.update_data["document_number"])
        self.assertEqual(obj.created, self.get_date(self.update_data["datevalue"]))
        self.assertEqual(len_qs, 1)


class InStockTopicDataHandlerTestCase(TestCase, BaseTestCase):
    fixtures = ("Nomenclature.json", "DataHandlersMap.json")

    def setUp(self):
        self.data = INSTOCKTOPIC_DATA

    def save_data(self):
        datahandler = DataHandlerFactory.get_handler(self.data, "FarmZakaz_Stock_test")
        datahandler.save_data()

    def test_save_data(self):
        self.save_data()
        obj = Residue.objects.first()
        self.assertEqual(obj.series, self.data["series_code"])
        self.assertEqual(obj.uid_batch, self.data["uid_batch"])

    def test_save_old_data(self):
        self.save_data()
        self.old_uid_batch = self.data.get("uid_batch")
        self.data.update({"uid_batch": "2"})
        self.save_data()
        obj = ResidueHistory.objects.first()
        self.assertEqual(obj.series, self.data["series_code"])
        self.assertEqual(obj.uid_batch, self.old_uid_batch)
        obj = Residue.objects.first()
        self.assertEqual(obj.series, self.data["series_code"])
        self.assertEqual(obj.uid_batch, self.data["uid_batch"])


class NomenclatureTopicDataHandlerTestCase(TestCase, BaseTestCase):
    fixtures = ("Nomenclature.json", "DataHandlersMap.json")

    def setUp(self):
        self.data = NOMENCLATURE

    def save_data(self):
        datahandler = DataHandlerFactory.get_handler(self.data, "FarmZakaz_Nomenclature_test")
        datahandler.save_data()

    def test_save_data(self):
        self.save_data()
        obj = Nomenclature.objects.get(code="00010")
        self.assertEqual(obj.gtin, self.data["GTIN"])
        self.assertEqual(obj.ean13, self.data["EAN13"])
        self.assertEqual(obj.name, self.data["name"])

    def test_update_data(self):
        self.save_data()
        self.old_gtin_batch = self.data.get("GTIN")
        self.data.update({"GTIN": "18901043000460"})
        self.save_data()
        obj = Nomenclature.objects.get(code="00010")
        self.assertEqual(obj.ean13, self.data["EAN13"])
        self.assertEqual(obj.gtin, self.data.get("GTIN"))


class LegalEntityOnboardedDataHandlerTestCase(TestCase, BaseTestCase):
    fixtures = ("LegalEntityOnboarded.json", "DataHandlersMap.json")

    def setUp(self):
        self.data = LEGAL_ENTITY_ONBOARDED

    def save_data(self):
        datahandler = DataHandlerFactory.get_handler(self.data, "FarmZakaz_Clients_test")
        datahandler.save_data()

    def test_save_data(self):
        self.save_data()
        obj = LegalEntityOnboarded.objects.get(ext_id="233")
        self.assertEqual(obj.status, self.data[0]["status"])
        self.assertEqual(obj.inn, self.data[0].get("inn"))
        self.assertEqual(obj.sended_to_pz, False)
        self.assertEqual(obj.sended_to_pz_at, None)

        obj = LegalEntityOnboarded.objects.get(ext_id="234")
        self.assertEqual(obj.status, self.data[1]["status"])
        self.assertEqual(obj.inn, self.data[1].get("inn"))
        self.assertEqual(obj.sended_to_pz, False)
        self.assertEqual(obj.sended_to_pz_at, None)
