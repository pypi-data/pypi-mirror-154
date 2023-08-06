import datetime

import pytz


class StoresRequestTestCaseData:
    list_response_get = {
        "count": 0,
        "next": None,
        "previous": None,
        "results": []
    }

    read_response_get = {
        'storeInfoId': 273581,
        'posId': None,
        'inn': '123456789999',
        'legalName': 'OOO Test 99',
        'fiasId': '770099',
        'fiasCode': '99',
        'federalDistrict': 'СВАО',
        'region': 'МО',
        'regionalDistrict': 'string',
        'city': 'Зеленоград',
        'street': 'Логвиненко',
        'building': '3',
        'fullAddress': 'string',
        'hasContract': False,
        'isBlacklist': False,
        'paymentDelay': '0',
        'posExtId': '12345',
        'created': '2022-01-20T15:23:58.074433+03:00',
        'warehouses': [{'warehouseId': 102}]
    }

    create_data_post = {
        "inn": "123456789012",
        "legalName": "OOO Test",
        "fiasId": "770077",
        "fiasCode": "0",
        "federalDistrict": "ЦАО",
        "region": "МО",
        "regionalDistrict": "string",
        "city": "Москва",
        "street": "string",
        "building": "3",
        "fullAddress": "string",
        "hasContract": False,
        "isBlacklist": False,
        "paymentDelay": 0,
        "posExtId": "12345",
        "warehouses": [{"warehouseId": 102}],
    }

    create_response_post = {
        'storeInfoId': 273581,
        'posId': None,
        'inn': '123456789012',
        'legalName': 'OOO Test',
        'fiasId': '770077',
        'fiasCode': '0',
        'federalDistrict': 'ЦАО',
        'region': 'МО',
        'regionalDistrict': 'string',
        'city': 'Москва',
        'street': 'string',
        'building': '3',
        'fullAddress': 'string',
        'hasContract': False,
        'isBlacklist': False,
        'paymentDelay': '0',
        'posExtId': '12345',
        'created': '2022-01-20T15:23:58.074433+03:00',
        'warehouses': [{'warehouseId': 102}]
    }

    partial_update_data_patch = {
        "inn": 123456789999,
        "legalName": "OOO Test 99",
        "fiasId": 770099,
        "fiasCode": 99,
        "federalDistrict": "СВАО",
        "region": "МО",
        "regionalDistrict": "string",
        "city": "Зеленоград",
        "street": "Логвиненко",
        "building": "3",
        "fullAddress": "string",
        "hasContract": False,
        "isBlacklist": False,
        "paymentDelay": 0,
        "posExtId": "54321",
        "warehouses": [
            {"warehouseId": 102}
        ]
    }

    partial_update_response_patch = {
        'storeInfoId': 273581,
        'inn': '123456789999',
        'legalName': 'OOO Test 99',
        'fiasId': '770099',
        'fiasCode': '99',
        'federalDistrict': 'СВАО',
        'region': 'МО',
        'regionalDistrict': 'string',
        'city': 'Зеленоград',
        'street': 'Логвиненко',
        'building': '3',
        'fullAddress': 'string',
        'hasContract': False,
        'isBlacklist': False,
        'paymentDelay': '0',
        'posExtId': '12345',
        'created': '2022-01-20T15:23:58.074433+03:00',
        'warehouses': [{'warehouseId': 102}]
    }

    get_read_list_stores = {
        'count': 3,
        'next': None,
        'previous': None,
        'results': [{
            'storeInfoId': 273691,
            'posId': 64345,
            'inn': '5404151808',
            'legalName': 'СП-Фарм ООО ФК',
            'fiasId': '0',
            'fiasCode': '0',
            'federalDistrict': 'Новосибирск',
            'region': 'Новосибирская обл',
            'regionalDistrict': 'Новосибирск',
            'city': 'Новосибирск',
            'street': 'ул Урманова',
            'building': '11',
            'fullAddress': 'ул Урманова, д, 11',
            'hasContract': True,
            'isBlacklist': False,
            'paymentDelay': '0',
            'posExtId': '0000001',
            'created': '2022-03-21T10:25:04.910854+03:00',
            'warehouses': [{
                'warehouseId': 130
            }
            ]
        }, {
            'storeInfoId': 274105,
            'posId': None,
            'inn': '6731044438',
            'legalName': 'ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО "СМОЛЕНСК-ФАРМАЦИЯ"',
            'fiasId': '0',
            'fiasCode': '0',
            'federalDistrict': 'Смоленская обл.',
            'region': 'Смоленская обл.',
            'regionalDistrict': 'Смоленская обл.',
            'city': 'Смоленск г',
            'street': 'Крупской ул',
            'building': '28',
            'fullAddress': '214019, Смоленская обл., г. Смоленск, ул. Крупской, д. 28',
            'hasContract': True,
            'isBlacklist': False,
            'paymentDelay': '60',
            'posExtId': 'БРН000013738',
            'created': '2022-03-30T12:26:50.219521+03:00',
            'warehouses': [{
                'warehouseId': 130
            }
            ]
        }, {
            'storeInfoId': 274047,
            'posId': None,
            'inn': '7801379023',
            'legalName': 'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "КЕДР"',
            'fiasId': '0',
            'fiasCode': '0',
            'federalDistrict': 'Смоленская обл',
            'region': 'Смоленская обл',
            'regionalDistrict': 'Смоленская обл',
            'city': 'Смоленск г',
            'street': 'Николаева ул',
            'building': '21',
            'fullAddress': '214004, Смоленская обл, Смоленск г, Николаева ул, дом № 21, помещения № 24-28',
            'hasContract': False,
            'isBlacklist': True,
            'paymentDelay': '999',
            'posExtId': 'БРН000016897',
            'created': '2022-03-28T15:53:40.095566+03:00',
            'warehouses': [
                {'warehouseId': 130}
            ]
        }
        ]
    }


class WarehousesRequestTestCaseData:
    list_response_get = {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [{
            'warehouseId': 102,
            'name': 'Склад МО',
            'address': 'Московская область, Ленинградская ул. 1',
            'extId': '000001',
            'extData': {}}]
    }

    read_response_get = {
        'warehouseId': 102,
        'name': 'Склад МО',
        'address': 'Московская область, Ленинградская ул. 1',
        'extId': '000001',
        'extData': {}
    }

    create_data_post = {
        "name": "Склад МО",
        "address": "Московская область, Ленинградская ул. 1 стр 1",
        "extId": "000002",
        "extData": {}
    }

    create_response_post = {
        'warehouseId': 102,
        'name': "Склад МО",
        'address': "Московская область, Ленинградская ул. 1 стр 1",
        'extId': "000002",
        'extData': {}
    }

    partial_update_data_patch = {
        'name': "Склад МО",
        'address': "Московская область, Ленинградская ул. 2 стр 2",
        'extId': "000002",
        'extData': {}
    }

    partial_update_response_patch = {
        'warehouseId': 102,
        'name': 'Склад МО',
        'address': 'Московская область, Ленинградская ул. 2 стр 2',
        'extId': '000002',
        'extData': {}
    }

    send_warehouses_data_post = {
        "name": "Test branch",
        "address": "Some address branch",
        "extId": "123456701",
        "extData": None
    }

    send_warehouses_response_post = {
        'warehouseId': 130,
        "name": "Test branch",
        "address": "Some address branch",
        "extId": "123456701",
        'extData': {}
    }


class OrdersRequestTestCaseData:
    list_response_get = {
        "count": 0,
        "next": None,
        "previous": "string",
        "results": [
            {
                "orderId": 0,
                "status": "new",
                "posExtId": "string",
                "created": "2022-01-19T13:28:32.210Z",
                "updated": "2022-01-19T13:28:32.210Z",
                "totalSum": 0,
                "vatSum": 0,
                "positions": [
                    {
                        "positionId": 0,
                        "gtin": "string",
                        "ean13": "string",
                        "series": "string",
                        "itemId": 0,
                        "quantity": 0,
                        "price": 0,
                        "vat": 0,
                        "expirationDate": "2022-01-19",
                        "extId": "string",
                        "invoiceNum": "string",
                        "warehouseExtId": "string"
                    }
                ]
            }
        ]
    }

    read_response_get = {
        "orderId": 0,
        "status": "string",
        "posExtId": "string",
        "created": "2022-01-19T13:29:13.363Z",
        "updated": "2022-01-19T13:29:13.363Z",
        "totalSum": 0,
        "vatSum": 0,
        "positions": [
            {
                "positionId": 0,
                "gtin": "string",
                "ean13": "string",
                "series": "string",
                "itemId": 0,
                "quantity": 0,
                "price": 0,
                "vat": 0,
                "expirationDate": "2022-01-19",
                "extId": "string",
                "invoiceNum": "string",
                "warehouseExtId": "string"
            }
        ]
    }

    partial_update_data_patch = {
        "status": "string",
        "positions": [
            {
                "series": "string",
                "itemId": 0,
                "quantity": 0,
                "price": 0,
                "invoiceNum": "string"
            }
        ]
    }

    partial_update_response_patch = {
        "orderId": 0,
        "status": "string",
        "posExtId": "string",
        "created": "2022-01-19T13:29:22.801Z",
        "updated": "2022-01-19T13:29:22.801Z",
        "totalSum": 0,
        "vatSum": 0,
        "positions": [
            {
                "positionId": 0,
                "gtin": "string",
                "ean13": "string",
                "series": "string",
                "itemId": 0,
                "quantity": 0,
                "price": 0,
                "vat": 0,
                "expirationDate": "2022-01-19",
                "extId": "string",
                "invoiceNum": "string",
                "warehouseExtId": "string"
            }
        ]
    }

    partial_returns_update_data_patch = {
        "positions": [
            {
                "itemId": 0,
                "quantity": 0
            }
        ]
    }

    partial_returns_update_response_patch = {
        "orderId": 0,
        "status": "string",
        "posExtId": "string",
        "created": "2022-01-19T13:29:33.843Z",
        "updated": "2022-01-19T13:29:33.843Z",
        "totalSum": 0,
        "vatSum": 0,
        "positions": [
            {
                "positionId": 0,
                "gtin": "string",
                "ean13": "string",
                "series": "string",
                "itemId": 0,
                "quantity": 0,
                "price": 0,
                "vat": 0,
                "expirationDate": "2022-01-19",
                "extId": "string",
                "invoiceNum": "string",
                "warehouseExtId": "string",
                "reason": "string"
            }
        ]
    }

    get_list_orders = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {
                "orderId": 255592,
                "status": "transmitted",
                "posExtId": "0000001",
                "created": "2022-04-22T12:45:35.937048+03:00",
                "updated": "2022-04-22T13:34:18.902801+03:00",
                "totalSum": 71292.37,
                "vatSum": 6481.12,
                "positions": [
                    {
                        "positionId": 726776,
                        "gtin": "04601969007411",
                        "ean13": "4601969007411",
                        "series": "",
                        "itemId": "0013b07a-5f1b-434b-81eb-71f772c81506",
                        "quantity": 823,
                        "price": 78.75,
                        "vat": 7.88,
                        "expirationDate": "2025-08-01",
                        "extId": "41023",
                        "invoiceNum": "",
                        "warehouseExtId": "3255510243"
                    }
                ]
            }
        ]
    }

    orders_request_params = {
        'warehouseId': 130,
        'limit': 100,
        'offset': 0,
        'status': 'new',
        'created_gte': datetime.date(2022, 2, 18)
    }

    order_update_data_patch = {
        'status': 'transmitted',
        'positions': [{
            'order': 'Order object (255453)',
            'GTIN': '04601969007428',
            'EAN13': '4601969007428',
            'itemId': '0c678231-cfe9-456d-ac5f-128ad519e7d6',
            'quantity': '0',
            'price': '198.45',
            'vat': '19.84',
            'expirationDate': '2025-02-01',
            'extId': '52218',
            'info_received': False
        }, {
            'order': 'Order object (255453)',
            'GTIN': '04601969007558',
            'EAN13': '4601969007558',
            'itemId': '3e9e5800-6e0c-48fd-ba23-5e0659a5ebaa',
            'quantity': '0',
            'price': '260.74',
            'vat': '26.07',
            'expirationDate': '2022-08-01',
            'extId': '48664',
            'info_received': False
        }, {
            'order': 'Order object (255453)',
            'GTIN': '04601969004496',
            'EAN13': '4601969004496',
            'itemId': '6e53be80-d52d-4a32-ad51-c62c3ff6bc3e',
            'quantity': '0',
            'price': '183.49',
            'vat': '18.35',
            'expirationDate': '2022-11-01',
            'extId': '48931',
            'info_received': False
        }, {
            'order': 'Order object (255453)',
            'GTIN': '04601969001082',
            'EAN13': '4601969001082',
            'itemId': 'e7cdd422-7ae6-47c8-b658-73c9fc6cbba6',
            'quantity': '0',
            'price': '255.19',
            'vat': '25.52',
            'expirationDate': '2025-12-01',
            'extId': '11081',
            'info_received': False
        }, {
            'order': 'Order object (255453)',
            'GTIN': '04601969005080',
            'EAN13': '4601969005080',
            'itemId': 'c50b76b9-dd3e-40f4-ae31-6f58399e38c6',
            'quantity': '0',
            'price': '229.44',
            'vat': '22.95',
            'expirationDate': '2023-08-01',
            'extId': '48672',
            'info_received': False
        }, {
            'order': 'Order object (255453)',
            'GTIN': '04601969007862',
            'EAN13': '4601969007862',
            'itemId': '1ac05f1e-7950-4603-b8f0-28bdee42298e',
            'quantity': '0',
            'price': '106.16',
            'vat': '10.62',
            'expirationDate': '2022-09-01',
            'extId': '45850',
            'info_received': False
        }, {
            'order': 'Order object (255453)',
            'GTIN': '04601969007527',
            'EAN13': '4601969007527',
            'itemId': 'f631f18a-0389-404d-81f5-89bcc2a38c7c',
            'quantity': '0',
            'price': '248.44',
            'vat': '24.84',
            'expirationDate': '2022-03-01',
            'extId': '43627',
            'info_received': False
        }, {
            'order': 'Order object (255453)',
            'GTIN': '04601969007442',
            'EAN13': '4601969007442',
            'itemId': '2783b4db-c685-4e6f-81ae-09f2dff669f1',
            'quantity': '0',
            'price': '203.52',
            'vat': '20.35',
            'expirationDate': '2022-09-01',
            'extId': '52219',
            'info_received': False
        }, {
            'order': 'Order object (255453)',
            'GTIN': '04601969005585',
            'EAN13': '4601969005585',
            'itemId': '9f82a2b3-57f3-464e-b413-5db1459ae550',
            'quantity': '0',
            'price': '391.95',
            'vat': '39.20',
            'expirationDate': '2023-01-01',
            'extId': '48467',
            'info_received': False
        }, {
            'order': 'Order object (255453)',
            'GTIN': '04601969003796',
            'EAN13': '4601969003796',
            'itemId': '77cc08c6-0e50-41dd-9614-56c40c9bfcdd',
            'quantity': '0',
            'price': '371.06',
            'vat': '37.11',
            'expirationDate': '2023-04-01',
            'extId': '48701',
            'info_received': False
        }
        ]
    }

    order_update_response_patch = {
        "orderId": 255453,
        "status": "transmitted",
        "posExtId": "20020738",
        "updated": "2022-02-18T12:09:42.629Z",
        "created": "2022-02-18T12:09:42.601Z",
        "totalSum": "16504.21",
        "vatSum": "1500.40",
        "positions": order_update_data_patch.get('positions')
    }

    kafka_msg = {
        '#type': 'jv8:Array',
        '#value': [{
            '#type': 'jv8:Structure',
            '#value': [{
                'name': {
                    '#type': 'jxs:string',
                    '#value': 'Идентификатор'
                },
                'Value': {
                    '#type': 'jv8:UUID',
                    '#value': 'f45a23dd-01ca-4a8e-8c8f-4e96cfee8ee2'
                }
            }, {
                'name': {
                    '#type': 'jxs:string',
                    '#value': 'Отправитель'
                },
                'Value': {
                    '#type': 'jxs:string',
                    '#value': 'PHZ'
                }
            }, {
                'name': {
                    '#type': 'jxs:string',
                    '#value': 'Получатель'
                },
                'Value': {
                    '#type': 'jxs:string',
                    '#value': 'БРН'
                }
            }, {
                'name': {
                    '#type': 'jxs:string',
                    '#value': 'Сервер'
                },
                'Value': {
                    '#type': 'jxs:string',
                    '#value': 'pharmzakaz.test'
                }
            }, {
                'name': {
                    '#type': 'jxs:string',
                    '#value': 'БазаДанных'
                },
                'Value': {
                    '#type': 'jxs:string',
                    '#value': 'PHZ'
                }
            }, {
                'name': {
                    '#type': 'jxs:string',
                    '#value': 'КлючДанных'
                },
                'Value': {
                    '#type': 'jxs:string',
                    '#value': 'ЗаказФЗ'
                }
            }
            ]
        }, {
            '#type': 'jxs:string',
            '#value': '[{"ИдЗаказа": 255454, "АдресДоставки": "20037703", "НомерСтроки": 1,'
                      ' "ИдентификаторСтроки": "db0476fa-283b-44ae-8e2e-d8c2f1f1c5c8",'
                      ' "Качество": "Кондиция", "Код": 55292, "КодДоп": 0, "КодТовараКонтрагента": "",'
                      ' "Количество": 4, "Наименование": "Моксонидин-Акрихин табл п/о плен 0,2 мг х30 АКЦИЯ пакет (5)",'
                      ' "Номенклатура": "Моксонидин-Акрихин табл п/о плен 0,2 мг х30 АКЦИЯ пакет (5)",'
                      ' "Производитель": "", "СпецПоставка": "", "СрокГодности": "2022-03-17",'
                      ' "Цена": 155.24, "ЦенаПлощадки": 155.24, "ЭлектронныйЗаказ": "",'
                      ' "Маркировка": "False"} ,  {"ИдЗаказа": 255454, "АдресДоставки": "20037703",'
                      ' "НомерСтроки": 2, "ИдентификаторСтроки": "f4e5d339-4b66-415b-84ef-e12e2021c12e",'
                      ' "Качество": "Кондиция", "Код": 57063, "КодДоп": 0, "КодТовараКонтрагента": "", "Количество": 4,'
                      ' "Наименование": "Гепарин-Акрихин 1000 гель 1000 МЕ/г туба 50 г х1 АКЦИЯ пакет (5)",'
                      ' "Номенклатура": "Гепарин-Акрихин 1000 гель 1000 МЕ/г туба 50 г х1 АКЦИЯ пакет (5)",'
                      ' "Производитель": "", "СпецПоставка": "", "СрокГодности": "2022-03-17", "Цена": 367.46,'
                      ' "ЦенаПлощадки": 367.46, "ЭлектронныйЗаказ": "", "Маркировка": "False"} ,'
                      '  {"ИдЗаказа": 255454, "АдресДоставки": "20037703", "НомерСтроки": 3,'
                      ' "ИдентификаторСтроки": "2aa77343-f104-4182-b7e5-eef64eede6b7", "Качество": "Кондиция",'
                      ' "Код": 49632, "КодДоп": 0, "КодТовараКонтрагента": "", "Количество": 5,'
                      ' "Наименование": "Венолайф Дуо табл п/о плен 1000 мг х30",'
                      ' "Номенклатура": "Венолайф Дуо табл п/о плен 1000 мг х30",'
                      ' "Производитель": "", "СпецПоставка": "", "СрокГодности": "2022-03-17",'
                      ' "Цена": 816.79, "ЦенаПлощадки": 816.79, "ЭлектронныйЗаказ": "", "Маркировка": "False"} ,'
                      '  {"ИдЗаказа": 255454, "АдресДоставки": "20037703", "НомерСтроки": 4,'
                      ' "ИдентификаторСтроки": "60aee11f-7b96-4b18-aee3-6a3939ff8b4e", "Качество": "Кондиция",'
                      ' "Код": 50449, "КодДоп": 0, "КодТовараКонтрагента": "", "Количество": 3,'
                      ' "Наименование": "Фенибут-Акрихин табл 250 мг х20 АКЦИЯ пакет (5)",'
                      ' "Номенклатура": "Фенибут-Акрихин табл 250 мг х20 АКЦИЯ пакет (5)",'
                      ' "Производитель": "", "СпецПоставка": "", "СрокГодности": "2022-03-17",'
                      ' "Цена": 163.24, "ЦенаПлощадки": 163.24, "ЭлектронныйЗаказ": "", "Маркировка": "False"} ,'
                      '  {"ИдЗаказа": 255454, "АдресДоставки": "20037703", "НомерСтроки": 5,'
                      ' "ИдентификаторСтроки": "cc041848-510c-4039-9fe6-b03007765631", "Качество": "Кондиция",'
                      ' "Код": 41906, "КодДоп": 0, "КодТовараКонтрагента": "", "Количество": 3,'
                      ' "Наименование": "Такропик мазь д/наруж прим 0,03% туба 15 г х1",'
                      ' "Номенклатура": "Такропик мазь д/наруж прим 0,03% туба 15 г х1",'
                      ' "Производитель": "", "СпецПоставка": "", "СрокГодности": "2022-03-17",'
                      ' "Цена": 520.0, "ЦенаПлощадки": 520.0, "ЭлектронныйЗаказ": "", "Маркировка": "False"} ,'
                      '  {"ИдЗаказа": 255454, "АдресДоставки": "20037703", "НомерСтроки": 6,'
                      ' "ИдентификаторСтроки": "7e7a31f2-2c1f-4170-830b-af0a40e88ce2", "Качество": "Кондиция",'
                      ' "Код": 58368, "КодДоп": 0, "КодТовараКонтрагента": "", "Количество": 5,'
                      ' "Наименование": "Гепарин-Акрихин 1000 гель 1000 МЕ/г 30 г х1 ^", '
                      '"Номенклатура": "Гепарин-Акрихин 1000 гель 1000 МЕ/г 30 г х1 ^",'
                      ' "Производитель": "", "СпецПоставка": "", "СрокГодности": "2022-03-17",'
                      ' "Цена": 256.73, "ЦенаПлощадки": 256.73, "ЭлектронныйЗаказ": "", "Маркировка": "False"}   ]'
        }
        ]
    }


class SKURequestTestCaseData:
    list_response_get = {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "extSkuId": "04492",
                "name": "Цитрамон П табл х6",
                "ean13": "4604060081014",
                "gtin": "string"
            }
        ]
    }

    create_data_post = [
        {
            "name": "Цитрамон П табл х6",
            "extSkuId": "04492",
            "ean13": "4604060081014"
        },
    ]

    read_response_get = {
        "extSkuId": "04492",
        "name": "Цитрамон П табл х6",
        "ean13": "4604060081014",
        "gtin": "string"
    }

    create_response_post = {
        "results": [
            {
                "name": "Цитрамон П табл х6",
                "extSkuId": "04492",
                "ean13": "4604060081014"
            }
        ],
        "errors": [
            "string"
        ]
    }

    patch_data = {
        "extSkuId": "04492"
    }

    patch_response = {
        "extSkuId": "04492",
        "name": "Цитрамон П табл х6",
        "ean13": "4604060081014",
        "gtin": "string"
    }

    sku_residues_list = {
        "ean13": "4604060081014",
        "gtin": "12345",
        "series": "string",
        "warehouseExtId": "102",
        "quantity": 1,
        "expirationDate": "2022-01-25",
        "extId": "string"
    }

    sku_residues_update_residues_list_data_post = [
        {
            "series": "12345",
            "warehouseExtId": "102",
            "quantity": 1,
            "expirationDate": "2022-01-19",
            "extId": "string"
        }
    ]

    sku_residues_update_residues_list_response_post = {
        "results": [
            {
                "ean13": "4604060081014",
                "gtin": "string",
                "series": "12345",
                "warehouseExtId": "102",
                "quantity": 1,
                "extId": "string"
            }
        ],
        "errors": [
            "string"
        ]
    }


class InvoicesRequestTestCaseData:
    list_response_get = {
        "invoiceId": 0,
        "invoiceNum": "string",
        "accepted": "2022-01-19",
        "delivered": "2022-01-19",
        "isAccept": True,
        "storeExtId": "string",
        "skuExtId": "string",
        "deliveredQuantity": 0,
        "deliveredSum": 0,
        "warehouseId": 0
    }

    read_response_get = {
        "invoiceId": 0,
        "invoiceNum": "string",
        "accepted": "2022-01-25",
        "delivered": "2022-01-25",
        "isAccept": True,
        "storeExtId": "string",
        "skuExtId": "string",
        "deliveredQuantity": 0,
        "deliveredSum": 0,
        "warehouseId": 0
    }

    create_data_post = {
        "invoiceNum": "string",
        "warehouseExtId": "string",
        "accepted": "2022-01-19",
        "delivered": "2022-01-19",
        "isAccept": True,
        "storeExtId": "string",
        "skuExtId": "string",
        "deliveredQuantity": 0,
        "deliveredSum": 0
    }

    create_response_post = {
        "invoiceId": 0,
        "invoiceNum": "string",
        "accepted": "2022-01-19",
        "delivered": "2022-01-19",
        "isAccept": True,
        "storeExtId": "string",
        "skuExtId": "string",
        "deliveredQuantity": 0,
        "deliveredSum": 0,
        "warehouseId": 0
    }

    partial_returns_update_data_patch = {
        "invoiceNum": "string",
        "warehouseExtId": "string",
        "accepted": "2022-01-25",
        "delivered": "2022-01-25",
        "isAccept": True,
        "storeExtId": "string",
        "skuExtId": "string",
        "deliveredQuantity": 0,
        "deliveredSum": 0
    }

    partial_returns_update_response_patch = {
        "invoiceId": 0,
        "invoiceNum": "string",
        "accepted": "2022-01-25",
        "delivered": "2022-01-25",
        "isAccept": True,
        "storeExtId": "string",
        "skuExtId": "string",
        "deliveredQuantity": 0,
        "deliveredSum": 0,
        "warehouseId": 0
    }

    test_create_invoice_data_post = {
        'invoiceNum': 'НСКР0115309',
        'warehouseExtId': '000002',
        'accepted': '2022-03-01',
        'delivered': '2022-02-28',
        'isAccept': None,
        'storeExtId': 'НСК000002506',
        'skuExtId': '02941',
        'deliveredQuantity': '2',
        'deliveredSum': '113.28'
    }

    test_create_invoice_response_post = {
        "invoiceId": 200,
        'invoiceNum': 'НСКР0115309',
        'warehouseExtId': '000002',
        'accepted': '2022-03-01',
        'delivered': '2022-02-28',
        'isAccept': None,
        'storeExtId': 'НСК000002506',
        'skuExtId': '02941',
        'deliveredQuantity': '2',
        'deliveredSum': '113.28'
    }

    test_list_invoice_response = {
        'count': 11,
        'next': None,
        'previous': None,
        'results': [{
            'invoiceId': 68,
            'invoiceNum': 'БРН00000006',
            'accepted': '2022-04-05',
            'delivered': '2022-04-02',
            'isAccept': True,
            'storeExtId': 'БРН000013736',
            'skuExtId': '56790',
            'deliveredQuantity': 5,
            'deliveredSum': 1657.87,
            'warehouseId': 130
        }, {
            'invoiceId': 70,
            'invoiceNum': 'БРН00000006',
            'accepted': '2022-04-05',
            'delivered': '2022-04-05',
            'isAccept': False,
            'storeExtId': 'БРН000013736',
            'skuExtId': '11081',
            'deliveredQuantity': 6,
            'deliveredSum': 1711.64,
            'warehouseId': 130
        }, {
            'invoiceId': 71,
            'invoiceNum': 'БРН00000006',
            'accepted': '2022-04-05',
            'delivered': '2022-04-05',
            'isAccept': False,
            'storeExtId': 'БРН000013736',
            'skuExtId': '09753',
            'deliveredQuantity': 6,
            'deliveredSum': 2000.26,
            'warehouseId': 130
        }, {
            'invoiceId': 72,
            'invoiceNum': 'БРН00000006',
            'accepted': '2022-04-05',
            'delivered': '2022-04-05',
            'isAccept': False,
            'storeExtId': 'БРН000013736',
            'skuExtId': '56790',
            'deliveredQuantity': 5,
            'deliveredSum': 1657.87,
            'warehouseId': 130
        }, {
            'invoiceId': 69,
            'invoiceNum': 'БРН00000007',
            'accepted': '2022-04-05',
            'delivered': '2022-04-05',
            'isAccept': False,
            'storeExtId': 'БРН000013736',
            'skuExtId': '13053',
            'deliveredQuantity': 10,
            'deliveredSum': 2589.95,
            'warehouseId': 130
        }, {
            'invoiceId': 73,
            'invoiceNum': 'БРН00000008',
            'accepted': '2022-04-07',
            'delivered': '2022-04-10',
            'isAccept': False,
            'storeExtId': 'БРН000013736',
            'skuExtId': '07920',
            'deliveredQuantity': 10,
            'deliveredSum': 4450.38,
            'warehouseId': 130
        }, {
            'invoiceId': 74,
            'invoiceNum': 'БРН00000008',
            'accepted': '2022-04-07',
            'delivered': '2022-04-10',
            'isAccept': False,
            'storeExtId': 'БРН000013736',
            'skuExtId': '09752',
            'deliveredQuantity': 9,
            'deliveredSum': 1946.84,
            'warehouseId': 130
        }, {
            'invoiceId': 75,
            'invoiceNum': 'БРН00000008',
            'accepted': '2022-04-07',
            'delivered': '2022-04-10',
            'isAccept': False,
            'storeExtId': 'БРН000013736',
            'skuExtId': '11081',
            'deliveredQuantity': 7,
            'deliveredSum': 1996.92,
            'warehouseId': 130
        }, {
            'invoiceId': 76,
            'invoiceNum': 'БРН00000008',
            'accepted': '2022-04-07',
            'delivered': '2022-04-10',
            'isAccept': False,
            'storeExtId': 'БРН000013736',
            'skuExtId': '56790',
            'deliveredQuantity': 6,
            'deliveredSum': 1989.44,
            'warehouseId': 130
        }, {
            'invoiceId': 80,
            'invoiceNum': 'БРН00000009',
            'accepted': '2022-04-11',
            'delivered': '2022-04-11',
            'isAccept': False,
            'storeExtId': 'БРН000013736',
            'skuExtId': '09753',
            'deliveredQuantity': 10,
            'deliveredSum': 3333.77,
            'warehouseId': 130
        }, {
            'invoiceId': 81,
            'invoiceNum': 'БРН00000009',
            'accepted': '2022-04-11',
            'delivered': '2022-04-11',
            'isAccept': False,
            'storeExtId': 'БРН000013736',
            'skuExtId': '56790',
            'deliveredQuantity': 10,
            'deliveredSum': 3315.73,
            'warehouseId': 130
        }
        ]
    }

    test_update_invoice_data_pathc = {
        'invoiceNum': 'БРН0012346',
        'warehouseExtId': '000002',
        'accepted': '2022-03-03',
        'delivered': '2022-02-28',
        'isAccept': False,
        'storeExtId': '20037703',
        'skuExtId': '55294',
        'deliveredQuantity': '10',
        'deliveredSum': '196.65'
    }

    test_update_invoice_response_patch = test_update_invoice_data_pathc


class BonusesRequestTestCaseData:
    accurals_list_response_get = {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "bonusId": 0,
                "accrualDate": "string",
                "period": "string",
                "inn": "string",
                "totalBonus": "string",
                "comment": "string",
                "isValid": "string",
                "statusDate": "string"
            }
        ]
    }

    payments_list_params_get = {
        "bonus_id": "3",
        "external_id": "1",
        "payment_order": "2",
        "bonus_payment_status": "123",
        "inn": "123456789",
        "period": "2022-01-25T08:25:56.083Z",
        "payment_date": "2022-01-25T08:25:56.083Z",
        "payment_date__lte": "2022-01-25T08:25:56.083Z",
        "payment_date__gte": "2022-01-25T08:25:56.083Z",
        "payment_date__lt": "2022-01-25T08:25:56.083Z",
        "payment_date__gt": "2022-01-25T08:25:56.083Z"
    }

    payments_list_response_get = {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "bonusId": 3,
                "bonusPaymentStatus": "string",
                "statusDate": "2022-01-25T08:25:56.083Z",
                "comment": "string",
                "paymentOrder": "2",
                "extId": 0,
                "id": 0
            }
        ]
    }

    create_data_post = {
        "bonusId": 3,
        "bonusPaymentStatus": "3",
        "statusDate": "2022-01-25T08:18:56.084Z",
        "comment": "string",
        "paymentOrder": "string",
        "extId": 0
    }

    create_response_post = {
        "bonusId": 3,
        "bonusPaymentStatus": "string",
        "statusDate": "2022-01-25T08:24:21.272Z",
        "comment": "string",
        "paymentOrder": "string",
        "extId": 0,
        "id": 0
    }


class LegalEntitiesTestCaseData:
    legal_entities_requests_list = {
        "count": 1,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "id": 43522,
                "created": "2022-01-25T09:22:21.088Z",
                "inn": "234234",
                "opf": "ООО",
                "legalEntity": "Аптека",
                "address": "ывыа",
                "fullName": "ыва",
                "position": "dd",
                "basisAuthority": "устав",
                "bic": "23634574",
                "bankAccount": "2262634634",
                "bank": "КРАСНОЯРСКОЕ ОТДЕЛЕНИЕ N 8646 ПАО СБЕРБАНК",
                "kppJuridicalPerson": "234234",
                "kppBank": "2343424",
                "correspondentAccount": "30101810800000000627",
                "status": "ACTUAL",
                "updated": "2022-03-15T13:19:09.680612+03:00"
            }
        ]
    }

    legal_entities_requests_list_with_changed_status = {
        "count": 1,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "id": 43522,
                "created": "2022-01-25T09:22:21.088Z",
                "inn": "234234",
                "opf": "ООО",
                "legalEntity": "Аптека",
                "address": "ывыа",
                "fullName": "ыва",
                "position": "dd",
                "basisAuthority": "устав",
                "bic": "23634574",
                "bankAccount": "2262634634",
                "bank": "КРАСНОЯРСКОЕ ОТДЕЛЕНИЕ N 8646 ПАО СБЕРБАНК",
                "kppJuridicalPerson": "234234",
                "kppBank": "2343424",
                "correspondentAccount": "30101810800000000627",
                "status": "NOT_ACTUAL",
                "updated": "2022-04-15T13:19:09.680612+03:00"
            }
        ]
    }

    legal_entities_list = {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "id": 0,
                "inn": "string",
                "contactSignDate": "2022-01-25T09:29:28.659Z",
                "status": "1",
                "statusUpdated": "2022-01-25T09:29:28.659Z",
                "extId": 0,
                "comment": "string"
            }
        ]
    }

    create_data_post = {
        "inn": "string",
        "contactSignDate": "2022-01-25T09:38:49.746Z",
        "status": "1",
        "statusUpdated": "2022-01-25T09:38:49.746Z",
        "extId": 0,
        "comment": "string"
    }

    create_response_post = {
        "id": 0,
        "inn": "string",
        "contactSignDate": "2022-01-25T09:38:49.764Z",
        "status": "1",
        "statusUpdated": "2022-01-25T09:38:49.764Z",
        "extId": 0,
        "comment": "string"
    }

    read_response_get = {
        "id": 1,
        "inn": "string",
        "contactSignDate": "2022-01-25T09:40:33.877Z",
        "status": "1",
        "statusUpdated": "2022-01-25T09:40:33.877Z",
        "extId": 0,
        "comment": "string"
    }

    partial_update_data_patch = {
        "inn": "string",
        "contactSignDate": "2022-01-25T09:42:45.930Z",
        "status": "1",
        "statusUpdated": "2022-01-25T09:42:45.930Z",
        "extId": 0,
        "comment": "string"
    }

    partial_update_response_patch = {
        "id": 1,
        "inn": "string",
        "contactSignDate": "2022-01-25T09:42:45.952Z",
        "status": "1",
        "statusUpdated": "2022-01-25T09:42:45.952Z",
        "extId": 0,
        "comment": "string"
    }


class ResudieTestCaseData:
    create_data_post = {
        '4601969000511': [
            {'GTIN': '04601969000511',
             'series': '10520',
             'EAN13': '4601969000511',
             'warehouseExtId': '3255510243',
             'quantity': '71',
             'expirationDate': '2024-05-01',
             'extId': 'b5e6125b-9a97-4768-878c-605a2d895efa',
             'skuExtId': '04164',
             'sended': False,
             'sended_at': None,
             'rest_time': None}],
        '4601969000580': [
            {'GTIN': '04601969000580',
             'series': '1111220',
             'EAN13': '4601969000580',
             'warehouseExtId': '3255510243',
             'quantity': '4550',
             'expirationDate': '2025-12-01',
             'extId': '1711c3d6-a7b6-43fb-a019-7840c105d68c',
             'skuExtId': '04175',
             'sended': False,
             'sended_at': None,
             'rest_time': None}]
    }

    create_response_post = {
        '4601969000511': {'results': [
            {'ean13': '4601969000511',
             'eanOther': None,
             'gtin': '04601969000511',
             'gtinOther': None,
             'series': '10520',
             'warehouseExtId': '3255510243',
             'quantity': 71,
             'expirationDate': '2024-05-01',
             'extId': 'b5e6125b-9a97-4768-878c-605a2d895efa',
             'skuExtId': '04164'}], 'errors': []},
        '4601969000580': {'results': [
            {'ean13': '4601969000580',
             'eanOther': None,
             'gtin': '04601969000580',
             'gtinOther': None,
             'series': '1111220',
             'warehouseExtId': '3255510243',
             'quantity': 4550,
             'expirationDate': '2025-12-01',
             'extId': '1711c3d6-a7b6-43fb-a019-7840c105d68c',
             'skuExtId': '04175'}], 'errors': []}
    }

    diff_residues = [(0, False, None, '04601969001075', '1061120', '4601969001075', '3255510243', 6640,
                      datetime.date(2025, 11, 1), '5f6d822b-6ae7-4e3e-b8cf-5c33580b4809', '04176',
                      '4d0a575d-c06d-43e6-8088-f0eedd4888eb',
                      datetime.datetime(2022, 4, 10, 11, 16, 41, 115000, tzinfo=pytz.utc),
                      datetime.datetime(2022, 4, 10, 11, 16, 41, 111000, tzinfo=pytz.utc))]
