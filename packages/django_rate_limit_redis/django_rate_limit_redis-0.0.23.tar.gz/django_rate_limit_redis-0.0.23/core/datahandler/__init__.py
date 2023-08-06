from django.utils.module_loading import import_string

from core.consts import ORDER_STATUSES_ONE_C
from core.models import DataHandlersMap
from core.models import Invoice
from core.models import LegalEntityOnboarded
from core.models import Nomenclature
from core.models import Order
from core.models import OrderStatusMap
from core.models import Position
from core.models import Residue
from core.models import ResidueHistory
from core.models import Store
from core.utils import parse_datetime


class UnknownDataHandler(Exception):
    pass


class UnsupportedMsgType(Exception):
    pass


class DataHandlerFactory:
    @classmethod
    def get_handler(cls, data, topic: str):
        try:
            data_handler = DataHandlersMap.objects.get(topic=topic).data_handler
            datahandler_cls = import_string(f"core.datahandler.{data_handler}")
        except Exception as ex:
            raise UnknownDataHandler(f"Data handler not found for topic: {topic}, ex: {ex}")

        datahandler = datahandler_cls(data, topic)
        return datahandler


class DataHandlerBase:
    def __init__(self, data, topic: str):
        self.data = data
        self.topic = topic

    def save_data(self):
        if isinstance(self.data, dict):
            self._save(self.data)
        elif isinstance(self.data, list):
            for value in self.data:
                self._save(value)
        else:
            raise UnsupportedMsgType("Message type not defined. Available types: dict, list")

    def _save(self, data):
        raise NotImplementedError


class InStockTopic(DataHandlerBase):
    data_model = Residue
    data_old_model = ResidueHistory

    def _save(self, data):
        sku = Nomenclature.objects.get(code=data.get("goodscode"))
        quantity = data.get("quantity")
        if quantity < 0:
            quantity = 0
        update_fields = dict(
            gtin=sku.gtin,
            nomenclature=sku.code,
            series=data.get("series_code"),
            ean13=sku.ean13,
            warehouse_ext_id=data.get("inn"),
            quantity=quantity,
            expiration_date=parse_datetime(data.get("expirationDate")),
            uid_batch=data.get("uid_batch")
        )
        old_residue = self.data_model.objects.filter(
            warehouse_ext_id=data.get("inn")
        ).exclude(
            uid_batch=data.get("uid_batch")
        )

        if old_residue:
            for obj in old_residue:
                obj_dict = obj.__dict__
                obj_dict.pop("_state")
                self.data_old_model.objects.create(**obj_dict)
            old_residue.delete()

        self.data_model.objects.create(**update_fields)


class OrdersTopic(DataHandlerBase):
    data_model = Order

    def __init__(self, data, topic: str):
        self.status_map = dict((y, x) for x, y in ORDER_STATUSES_ONE_C)
        super().__init__(data, topic)

    def _save(self, data):
        obj = self.data_model.objects.get(order_id=data.get("orderId"))

        status_one_c = data.get("status")
        if status_one_c in self.status_map:
            status_pz = self.status_map.get(status_one_c)
            try:
                status = OrderStatusMap.objects.get(status_one_c=status_pz).status_pharm_zakaz
            except OrderStatusMap.DoesNotExist as exc:
                raise Exception(exc, "No match found for statuses in table: OrderStatusMap")
            else:
                obj.status = status
                obj.store_ext_id = data.get("address_code")
                obj.warehouse_ext_id = data.get("inn")
                obj.total_sum = data.get("checksum_total")
                obj.vat_sum = data.get("total_VAT")
                obj.document_number = data.get("document_number")
                obj.save()

                update_pos_fields = dict(
                    series=data.get("series_code"),
                    quantity=data.get("quantity"),
                    info_received=True
                )

                price_vat = data.get("price_with_VAT")
                price = data.get("price")

                if price and price_vat:
                    vat = price_vat - price
                    update_pos_fields.update({
                        "price": price,
                        "vat": vat,
                    })

                positions = Position.objects.filter(
                    order_id=data.get("orderId"),
                    ext_id=data.get('goodscode'),
                )
                if positions.exists():
                    positions.update(**update_pos_fields)

        else:
            raise Exception(f"Status 1C not found in status constants {status_one_c}")


class SalesTopicV2(DataHandlerBase):
    data_model = Invoice

    def _save(self, data):
        order_id = data.get("orderId")
        document_number = data.get("document_number")
        goods_code = data.get("goodscode")

        update_fields = dict(
            delivered=parse_datetime(data.get("delivered")),  # TODO проверить что добавили в топик
            created=parse_datetime(data.get("datevalue")),
            is_accept=data.get("isAccept", False),
            store_ext_id=data.get("address_code"),
            delivered_quantity=data.get("quantity"),
            delivered_sum=data.get("checksum_total"),
            sended=False,
            order_ext_id=order_id,
            warehouse_ext_id=data.get("inn"),
        )
        self.data_model.objects.update_or_create(
            invoice_num=document_number,
            sku_ext_id=goods_code,
            defaults=update_fields
        )
        if order_id:
            positions_qs = Position.objects.filter(order_id=order_id, ext_id=goods_code)
            if positions_qs.exists():
                for position in positions_qs:
                    if position.invoice_num:
                        if document_number not in position.invoice_num:
                            position.invoice_num = '; '.join([position.invoice_num, document_number])
                    else:
                        position.invoice_num = document_number
                    position.save()


class NomenclatureTopic(DataHandlerBase):
    data_model = Nomenclature

    def _save(self, data):
        update_fields = dict(
            gtin=data.get("GTIN"),
            ean13=data.get("EAN13"),
            code=data.get("goodscode"),
            name=data.get("name"),
            sended=False,
        )

        self.data_model.objects.update_or_create(
            code=data.get("goodscode"),
            defaults=update_fields
        )


class StoreTopic(DataHandlerBase):
    data_model = Store

    def _save(self, data):
        full_address = f'{data.get("Index")}' \
                       f' {data.get("region")}' \
                       f' {data.get("city")}' \
                       f' {data.get("street")}' \
                       f' {data.get("building")}'
        ext_id = data.get("extId")
        update_fields = dict(
            inn=data.get("INN"),
            legal_name=data.get("legalName"),
            fias_id=data.get("fias_id", 0),
            fias_code=data.get("fias_code", 0),
            federal_district=data.get("federal_district", data.get("region")),
            region=data.get("region"),
            regional_district=data.get("regional_district", data.get("region")),
            city=data.get("city"),
            street=data.get("street"),
            building=data.get("building"),
            full_address=data.get("full_address", full_address),
            has_contract=data.get("hasContract"),
            black_list=data.get("isBlackList"),
            payment_delay=data.get("paymentDelay"),
            pos_ext_id=ext_id,
            branch=data.get("warehouses"),
            sended=False,
        )
        self.data_model.objects.update_or_create(
            pos_ext_id=ext_id,
            defaults=update_fields
        )


class LegalEntitiesOnboardedTopic(DataHandlerBase):
    data_model = LegalEntityOnboarded

    def _save(self, data):
        '''
           {
              "inn": "string",
              "contactSignDate": "2022-03-18T12:12:45.982Z",
              "status": "FORMED",
              "statusUpdated": "2022-03-18T12:12:45.982Z",
              "extId": 0,
              "comment": "string"
            }
        '''
        qs = self.data_model.objects.filter(ext_id=data.get("extId"))  # идентификатор на стороне 1C
        if qs.exists():
            qs.update(
                status=data.get("status"),
                status_updated=data.get("statusUpdated"),
                sended_to_pz=False,
                sended_to_pz_at=None,
            )
        else:
            self.data_model.objects.create(
                inn=data.get("inn"),
                contact_sign_date=data.get("contactSignDate"),
                status=data.get("status"),
                status_updated=data.get("statusUpdated"),
                ext_id=data.get("extId"),
                comment=data.get("comment"),
                sended_to_pz=False,
                sended_to_pz_at=None,
            )


TOPIC_MAP = {
    "FarmZakaz_Stock_test": InStockTopic,
    "orderstopic": OrdersTopic,
    "salestopicV2": SalesTopicV2,
    "FarmZakaz_Nomenclature_test": NomenclatureTopic,
    "FarmZakaz_Adresa_test": StoreTopic,
    "FarmZakaz_Clients_test": LegalEntitiesOnboardedTopic,
}
