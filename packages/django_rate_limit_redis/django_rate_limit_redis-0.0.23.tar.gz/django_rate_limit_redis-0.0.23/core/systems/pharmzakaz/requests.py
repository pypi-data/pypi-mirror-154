import abc
import json
from typing import Dict

from rate_limit.decorators import rate_limit
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from django.conf import settings

from core.apm import request_apm_trace
from core.models import ErrorsRequest

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RequestPaginationMixin:
    params: Dict
    page_size = 100  # TODO Перенести в настройки

    def set_page(self, page: int):
        self.params.update({"limit": self.page_size, "offset": self.page_size * page})
        return self

    def next_page(self):
        offset = self.params.get("offset")
        if offset >= 0:
            offset += self.page_size
        else:
            offset = 0
        self.params.update({"limit": self.page_size, "offset": offset})
        return self


class RequestBase(abc.ABC, RequestPaginationMixin):
    params = {}
    data = {}
    user = None
    password = None
    verify = False

    def __init__(self, method: str):
        self.method = method
        # "https://demo.pharm-zakaz.ru/api/distributor/v1/"
        # "https://pharm-zakaz.ru/distributor-api/v0/"
        self.endpoint = settings.PHARMZAKAZENDPOINT
        self.access_token = settings.PHARMZAKAZTOKEN
        self.url = self.endpoint + self.method
        self.base_url = self.endpoint + self.method
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def __str__(self) -> str:
        request_data = {
            "jsonrpc": "2.0",
            "method": self.method,
            "params": self.data,
            "id": 0,
        }
        return json.dumps(request_data)

    def save_error_request(self, errors, status_code, request_name):
        ErrorsRequest.objects.create(
            error=str(errors)[:500],
            status_code=status_code,
            request=request_name
        )

    def check_response(self, response, url):
        if response.status_code >= 500:
            self.save_error_request(str(response), response.status_code, url)

    @request_apm_trace
    @rate_limit(system="pharmzakaz", request_method="GET")
    def request_get(self, url, headers=None, data=None, params=None, auth=None):
        if not headers:
            headers = self.headers
        if not data:
            data = self.data
        if not params:
            params = self.params
        response = requests.get(url, headers=headers, data=json.dumps(data), params=params,
                                auth=auth, verify=self.verify)
        self.check_response(response, url)
        return response

    @request_apm_trace
    @rate_limit(system="pharmzakaz", request_method="POST")
    def request_post(self, url, headers=None, data=None, params=None, auth=None):
        response = requests.post(url, headers=self.headers, data=json.dumps(self.data), params=self.params,
                                 auth=auth, verify=self.verify)
        self.check_response(response, url)
        return response

    @request_apm_trace
    @rate_limit(system="pharmzakaz", request_method="PATCH")
    def request_patch(self, url, headers=None, data=None, params=None, auth=None):
        response = requests.patch(url, headers=self.headers, data=json.dumps(self.data), params=self.params,
                                  auth=auth, verify=self.verify)
        self.check_response(response, url)
        return response

    @request_apm_trace
    @rate_limit(system="pharmzakaz", request_method="PUT")
    def request_put(self, url, headers=None, data=None, params=None, auth=None):
        response = requests.put(url, headers=self.headers, data=json.dumps(self.data), params=self.params,
                                auth=auth, verify=self.verify)
        self.check_response(response, url)
        return response

    def next(self, url):
        return self.request_get(url)


class StoresRequest(RequestBase):
    """
    StoresRequest - Класс работы с аптеками ФЗ
    """

    def __init__(self):
        method = "stores/"
        super().__init__(method)

    def stores_list(self, warehouseId=0):
        """ GET /stores/
        Возвращает список аптек, привязанных к дистрибьютору.
        """
        if not self.params:
            offset = 0
            limit = 100
            self.params = {"warehouseId": warehouseId, "limit": limit, "offset": offset, }
        self.base_url = self.url
        return self.request_get(self.url)

    def stores_create(self, inn, legalName, fiasId, fiasCode, federalDistrict, region,
                      regionalDistrict, city, street, building, fullAddress, hasContract: bool,
                      isBlacklist: bool, paymentDelay, posExtId, warehouseId=None, warehouses=None):
        """ POST /stores/
        Создает новую аптеку с договором поставки с дистрибьютором.
        """
        if warehouseId:
            warehouses = [{"warehouseId": warehouseId}]
        self.data = {
            "inn": inn,
            "legalName": legalName,
            "fiasId": fiasId,
            "fiasCode": fiasCode,
            "federalDistrict": federalDistrict,
            "region": region,
            "regionalDistrict": regionalDistrict,
            "city": city,
            "street": street,
            "building": building,
            "fullAddress": fullAddress,
            "hasContract": hasContract,
            "isBlacklist": isBlacklist,
            "paymentDelay": paymentDelay,
            "posExtId": posExtId,
            "warehouses": warehouses,
        }
        self.base_url = self.url
        return self.request_post(self.url)

    def stores_read(self, storeInfoId):
        """ GET /stores/{storeInfoId}/
        Возвращает информацию об аптеке по storeInfoId.
        """
        self.base_url = f"{self.url}" + "{storeInfoId}/"
        return self.request_get(f"{self.url}{storeInfoId}/")

    def stores_partial_update(self, storeInfoId, inn, legalName, fiasId, fiasCode, federalDistrict, region,
                              regionalDistrict, city, street, building, fullAddress, hasContract: bool,
                              isBlacklist: bool, paymentDelay, posExtId, warehouseId=None, warehouses=None):
        """ PATCH /stores/{storeInfoId}/
        Изменяет информацию об аптеке.
        """
        if warehouseId:
            warehouses = [{"warehouseId": warehouseId}]
        self.data = {
            "inn": inn,
            "legalName": legalName,
            "fiasId": fiasId,
            "fiasCode": fiasCode,
            "federalDistrict": federalDistrict,
            "region": region,
            "regionalDistrict": regionalDistrict,
            "city": city,
            "street": street,
            "building": building,
            "fullAddress": fullAddress,
            "hasContract": hasContract,
            "isBlacklist": isBlacklist,
            "paymentDelay": paymentDelay,
            "posExtId": posExtId,
            "warehouses": warehouses,
        }
        self.base_url = f"{self.url}" + "{storeInfoId}/"
        return self.request_patch(f"{self.url}{storeInfoId}/")


class SKURequest(RequestBase):
    def __init__(self):
        method = "sku/"
        super().__init__(method)

    def sku_list(self):
        """ GET /sku/
        Возвращает список товаров (SKU), доступных для заказа у дистрибьютора.
        """
        if not self.params:
            offset = 0
            limit = 100
            self.params = {"limit": limit, "offset": offset, }
        self.base_url = self.url
        return self.request_get(self.url)

    def sku_update_sku_list(self, gtin=None, name=None, extSkuId=None, ean13=None, sku_list=None):
        """ POST /sku/update/
        Обновляет список SKU доступных для заказа у дистрибьютора.
        При ошибке обновления возвращает 200 код и структуру
        {'results': [], 'errors': ['Ean13=ean13 sku does not exists.']}
        """
        if sku_list:
            self.data = sku_list
        elif name and extSkuId and ean13:
            self.data = [
                {
                    "GTIN": gtin,
                    "name": name,
                    "extSkuId": extSkuId,
                    "EAN13": ean13
                },
            ]
        else:
            return
        self.base_url = f"{self.url}update/"
        return self.request_post(f"{self.url}update/")

    def sku_read(self, ean13):
        """ GET /sku/{EAN13}/
        Запрос по EAN-13.
        Возвращает код GTIN, код в системе дистрибьютора и название по каждому товару (SKU).
        """
        self.base_url = self.url + '{EAN13}/'
        return self.request_get(f"{self.url}{ean13}/")

    def sku_partial_update(self, ean13, extSkuId):
        """ PATCH /sku/{EAN13}/
        Изменяет SKU по коду EAN13.
        """
        self.data = {"extSkuId": extSkuId}
        self.base_url = self.url + '{ean13}/'
        return self.request_patch(f"{self.url}{ean13}/")

    def sku_residues_list(self, ean13, warehouseId):
        """ GET /sku/{EAN13}/residues/
        Возвращает список остатков SKU у дистрибьютора.
        """
        self.params = {"warehouseId": warehouseId}
        self.base_url = self.url + '{ean13}/residues/'
        return self.request_get(f"{self.url}{ean13}/residues/")

    def sku_residues_update_residues_list(self, ean13, series=None, warehouseExtId=None, quantity=None,
                                          expirationDate=None, extId=None, SkuExtId=None, sku_residues_list=None):
        """ POST /sku/{EAN13}/residues/update/
        Обновляет список остатков SKU доступных для заказа у дистрибьютора.
        """
        if sku_residues_list:
            self.data = sku_residues_list
        elif series and warehouseExtId and quantity and extId:
            self.data = [
                {
                    "series": series,
                    "warehouseExtId": warehouseExtId,
                    "quantity": quantity,
                    "expirationDate": expirationDate,
                    "extId": extId,
                    "SkuExtId": SkuExtId,
                },
            ]
        self.base_url = self.url + '{ean13}/residues/update/'
        return self.request_post(f"{self.url}{ean13}/residues/update/")


class WarehousesRequest(RequestBase):
    def __init__(self):
        method = "warehouses/"
        super().__init__(method)

    def warehouses_list(self):
        """ GET /warehouses/
        Получение списка складов дистрибьютора, добавленных в системе Фарм - Заказ.
        """
        if not self.params:
            offset = 0
            limit = 100
            self.params = {"limit": limit, "offset": offset, }
        self.base_url = self.url
        return self.request_get(self.url)

    def warehouses_create(self, name=None, address=None, extId=None, extData=None):
        """ POST /warehouses/
        Добавление склада дистрибьютора в системе Фарм - Заказ.
        """
        self.data = {
            "name": name,
            "address": address,
            "extId": extId,
            "extData": extData
        }
        self.base_url = self.url
        return self.request_post(self.url)

    def warehouses_read(self, warehouseId):
        """ GET /warehouses/{warehouseId}/
        Получение склада по id в системе Фарм-Заказ.
        """
        self.base_url = self.url + '{warehouseId}/'
        return self.request_get(f"{self.url}{warehouseId}/")

    def warehouses_partial_update(self, warehouseId, name=None, address=None, extId=None, extData=None):
        """ PATCH /warehouses/{warehouseId}/
        Обновление склада по id в системе Фарм - Заказ, для которого необходимо обновить информацию.
        """
        self.data = {
            "name": name,
            "address": address,
            "extId": extId,
            "extData": extData
        }
        self.base_url = self.url + '{warehouseId}/'
        return self.request_patch(f"{self.url}{warehouseId}/")

    def warehouses_residue_list(self, warehouseId):
        """ GET /warehouses/{warehouseId}/residues/
        Получение списка остатков на складе дистрибьютора.
        """
        if not self.params:
            offset = 0
            limit = 200
            self.params = {"limit": limit, "offset": offset, }
        self.base_url = self.url + '{warehouseId}/residues/'
        return self.request_get(f'{self.url}{warehouseId}/residues/')


class OrdersRequest(RequestBase):
    def __init__(self):
        method = "orders/"
        super().__init__(method)

    def orders_list(self, warehouseId, add_params=None):
        """GET /orders/
        Получение списка заказов для дистрибьютора.
        """
        if not self.params:
            offset = 0
            limit = 100
            self.params = {"warehouseId": warehouseId, "limit": limit, "offset": offset, }
        if add_params:
            self.params.update(**add_params)
        self.base_url = self.url
        return self.request_get(self.url)

    def orders_read(self, orderId):
        """ GET /orders/{orderId}/
        Получает заказ по orderid.
        """
        self.base_url = self.url + '{orderId}/'
        return self.request_get(f"{self.url}{orderId}/")

    def orders_partial_update(self, orderId, status=None, series=None,
                              itemId=None, quantity=None, price=None, invoiceNum=None, positions=None):
        """ PATCH /orders/{orderId}/
        Обновление статуса и/или состава заказа дистрибьютора.
        """
        if positions:
            self.data = {
                "status": status,
                "positions": positions}
        else:
            self.data = {
                "status": status,
                "positions": [
                    {
                        "series": series,
                        "itemId": itemId,
                        "quantity": quantity,
                        "price": price,
                        "invoiceNum": invoiceNum}
                ]
            }

        self.base_url = self.url + '{orderId}/'
        return self.request_patch(f"{self.url}{orderId}/")

    def orders_returns_update(self, orderId, itemId=None, quantity=None, positions=None):
        """ PATCH /orders/{orderId}/returns/
        Передача информации о полном возврате заказа.
        """
        if positions:
            self.data = {
                "positions": positions
            }
        else:
            self.data = {
                "positions": [
                    {
                        "itemId": itemId,
                        "quantity": quantity
                    }
                ]
            }
        self.base_url = self.url + '{orderId}/returns/'
        return self.request_patch(f"{self.url}{orderId}/returns/")


class InvoicesRequest(RequestBase):
    def __init__(self):
        method = "invoices/"
        super().__init__(method)

    def invoices_list(self, warehouseId=0):
        """ GET /invoices/
        Получение списка накладных дистрибьютора.
        """
        if not self.params:
            offset = 0
            limit = 100
            self.params = {"warehouseId": warehouseId, "limit": limit, "offset": offset, }
        self.base_url = self.url
        return self.request_get(self.url)

    def invoices_create(self, invoiceNum=None, warehouseExtId=None, accepted=None, delivered=None,
                        isAccept=None, storeExtId=None, skuExtId=False, deliveredQuantity=False, deliveredSum=None):
        """ POST /invoices/
        Создает новую накладную дистрибьютора.
        """
        self.data = {
            "invoiceNum": invoiceNum,
            "warehouseExtId": warehouseExtId,
            "accepted": accepted,
            "delivered": delivered,
            "isAccept": isAccept,
            "storeExtId": storeExtId,
            "skuExtId": skuExtId,
            "deliveredQuantity": deliveredQuantity,
            "deliveredSum": deliveredSum
        }
        self.base_url = self.url
        return self.request_post(self.url)

    def invoices_read(self, invoiceId):
        """ GET /invoices/{invoiceId}/
        Получает накладную дистрибьютора по id.
        """
        self.base_url = self.url + '{invoiceId}/'
        return self.request_get(f"{self.url}{invoiceId}/")

    def invoices_partial_update(self, invoiceId, invoiceNum=None, warehouseExtId=None,
                                accepted=None, delivered=None, isAccept=None, storeExtId=None,
                                skuExtId=False, deliveredQuantity=False, deliveredSum=None):
        """ PATCH /invoices/{id}/
        Изменяет накладную дистрибьютора по id.
        """
        self.data = {
            "invoiceNum": invoiceNum,
            "warehouseExtId": warehouseExtId,
            "accepted": accepted,
            "delivered": delivered,
            "isAccept": isAccept,
            "storeExtId": storeExtId,
            "skuExtId": skuExtId,
            "deliveredQuantity": deliveredQuantity,
            "deliveredSum": deliveredSum
        }
        self.base_url = self.url + '{invoiceId}/'
        return self.request_patch(f"{self.url}{invoiceId}/")


class BonusesRequest(RequestBase):
    """
    BonusPaymentStatus
    1 - Акт сформирован в системе дистрибьютора
    2 - Акт передан на подписание
    3 - Акт подписан аптечным учреждением
    4 - Выплата оформлена в системе дистрибьютора
    5 - Выплачено
    6 - Ошибка
    """
    BonusPaymentStatusList = ["1", "2", "3", "4", "5", "6"]

    def __init__(self):
        method = "bonuses/"
        super().__init__(method)

    def bonuses_accurals_list(self):
        """ GET /bonuses/accurals/
        Получение списка начисленных бонусов для выплаты через дистрибьютора.
        """
        if not self.params:
            offset = 0
            limit = 100
            self.params = {"limit": limit, "offset": offset, }
        self.base_url = f"{self.url}accurals/"
        return self.request_get(f"{self.url}accurals/")

    def bonuses_payments_list(self, bonus_id=None, external_id=None, payment_order=None, bonus_payment_status=None,
                              inn=None, period=None, payment_date=None, payment_date__lte=None, payment_date__gte=None,
                              payment_date__lt=None, payment_date__gt=None):
        """ GET /bonuses/payments/
        Получение списка выплаченных бонусов дистрибьютором.
        """
        if not self.params:
            offset = 0
            limit = 100
            self.params = {"limit": limit, "offset": offset, }

        if bonus_id:
            self.params.update({"bonus_id": bonus_id})
        if external_id:
            self.params.update({"external_id": external_id})
        if payment_order:
            self.params.update({"payment_order": payment_order})
        if bonus_payment_status:
            self.params.update({"bonus_payment_status": bonus_payment_status})
        if inn:
            self.params.update({"inn": inn})
        if period:
            self.params.update({"period": period})
        if payment_date:
            self.params.update({"payment_date": payment_date})
        if bonus_payment_status:
            self.params.update({"bonus_payment_status": bonus_payment_status})
        if payment_date__lte:
            self.params.update({"payment_date__lte": payment_date__lte})
        if payment_date__gte:
            self.params.update({"payment_date__gte": payment_date__gte})
        if payment_date__lt:
            self.params.update({"payment_date__lt": payment_date__lt})
        if payment_date__gt:
            self.params.update({"payment_date__gt": payment_date__gt})

        self.base_url = f"{self.url}payments/"
        return self.request_get(f"{self.url}payments/")

    def bonuses_payments_create(self, bonusId, bonusPaymentStatus, statusDate, comment=None, paymentOrder=None,
                                extId=None, data=None):
        """ PUT /bonuses/payments/{bonusId}/
        Загрузить новую запись со статусом выплаты бонусов.
        """
        if bonusPaymentStatus not in self.BonusPaymentStatusList:
            raise Exception(f"bonusPaymentStatus not supported. Please check the bonusPaymentStatus, "
                            f"Available statuses: {self.BonusPaymentStatusList}")
        if data:
            self.data = data
        else:
            self.data = {
                "bonusId": bonusId,
                "bonusPaymentStatus": bonusPaymentStatus,
                "statusDate": statusDate,
                "comment": comment,
                "paymentOrder": paymentOrder,
                "extId": extId
            }
        self.base_url = self.url + 'payments/{bonusId}/'
        return self.request_put(f"{self.url}payments/{bonusId}/")

    def bonuses_payments_update(self, bonusId, bonusPaymentStatus, statusDate, comment=None, paymentOrder=None,
                                extId=None, data=None):
        """ PATCH /bonuses/payments/{bonusId}/
        Обновить статус выплаты бонусов по ID.
        """
        if bonusPaymentStatus not in self.BonusPaymentStatusList:
            raise Exception(f"bonusPaymentStatus not supported. Please check the bonusPaymentStatus, "
                            f"Available statuses: {self.BonusPaymentStatusList}")

        if data:
            self.data = data
        else:
            self.data = {
                "bonusId": bonusId,
                "bonusPaymentStatus": bonusPaymentStatus,
                "statusDate": statusDate,
                "comment": comment,
                "paymentOrder": paymentOrder,
                "extId": extId
            }
        self.base_url = self.url + 'payments/{bonusId}/'
        return self.request_patch(f"{self.url}payments/{bonusId}/")


class LegalEntitiesRequest(RequestBase):
    def __init__(self):
        method = "legal-entities/"
        super().__init__(method)

    def legal_entities_list(self):
        """ GET /legal-entities/
        Список с данными о контрактах с юридическими лицами
        """
        if not self.params:
            offset = 0
            limit = 100
            self.params = {"limit": limit, "offset": offset, }
        self.base_url = self.url
        return self.request_get(self.url)

    def legal_entities_requests_list(self, add_params=None):
        """ GET /legal-entities/requests/
        Список юридических лиц запросивших заключение контракта.
        """
        if not self.params:
            offset = 0
            limit = 100
            self.params = {"limit": limit, "offset": offset, }

        if add_params:
            self.params.update(**add_params)

        self.base_url = f"{self.url}requests/"
        return self.request_get(f"{self.url}requests/")

    def legal_entities_create(self, inn=None, contactSignDate=None, status=None,
                              statusUpdated=None, extId=None, comment=None):
        """ POST /legal-entities/
        Создает новую запись о контракте с юридическим лицом.
        """
        self.data = {
            "inn": inn,
            "contactSignDate": contactSignDate,
            "status": status,
            "statusUpdated": statusUpdated,
            "extId": extId,
            "comment": comment
        }
        self.base_url = self.url
        return self.request_post(self.url)

    def legal_entities_read(self, id):
        """ GET /legal-entities/{id}/
        Данные о контракте с юридическим лицом по внутрннему id.
        """
        self.base_url = self.url + '{id}/'
        return self.request_get(f"{self.url}{id}/")

    def legal_entities_partial_update(self, id, inn=None, contactSignDate=None, status=None,
                                      statusUpdated=None, extId=None, comment=None):
        """ PATCH /legal-entities/{id}/
        Обновление статуса и/или состава заказа дистрибьютора.
        """
        self.data = {
            "inn": inn,
            "contactSignDate": contactSignDate,
            "status": status,
            "statusUpdated": statusUpdated,
            "extId": extId,
            "comment": comment
        }
        self.base_url = self.url + '{id}/'
        return self.request_patch(f"{self.url}{id}/")
