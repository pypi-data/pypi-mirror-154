NULLABLE = dict(blank=True, null=True)

"""
Возможные статусы заказа:
new - Новый,
equipped - Укомплектован,
confirmed - Подтвержден,
assembly - Передан На Сборку,
blocked - Заблокирован,
sent - Отправлен,
delivered - Доставлен,
refund - Возврат,
canceled - Отменен,
transmitted - Получен Дистрибьютором.
"""

# ORDER_STATUS_NEW = 1
# ORDER_DISTRIBUTOR_RECEIVED = 2
# ORDER_CONFIRMED = 3
# ORDER_TRANSFERRED_TO_ASSEMBLY = 4
# ORDER_STAFFED = 5
# ORDER_SENT = 6
# ORDER_DELIVERED = 7
# ORDER_CANCELED = 8
# ORDER_BLOCKED = 9
# ORDER_RETURN = 10

ORDER_STATUS_NEW = 'new'
ORDER_DISTRIBUTOR_RECEIVED = 'transmitted'
ORDER_CONFIRMED = 'confirmed'
ORDER_TRANSFERRED_TO_ASSEMBLY = 'assembly'
ORDER_STAFFED = 'equipped'
ORDER_SENT = 'sent'
ORDER_DELIVERED = 'delivered'
ORDER_CANCELED = 'canceled'
ORDER_BLOCKED = 'blocked'
ORDER_RETURN = 'refund'

ORDER_STATUSES = (
    (ORDER_STATUS_NEW, 'Новый'),
    (ORDER_DISTRIBUTOR_RECEIVED, 'ПолученДистрибьютором'),
    (ORDER_CONFIRMED, 'Подтвержден'),
    (ORDER_TRANSFERRED_TO_ASSEMBLY, 'ПереданНаСборку'),
    (ORDER_STAFFED, 'Укомплектован'),
    (ORDER_SENT, 'Отправлен'),
    (ORDER_DELIVERED, 'Доставлен'),
    (ORDER_CANCELED, 'Отменен'),
    (ORDER_BLOCKED, 'Заблокирован'),
    (ORDER_RETURN, 'Возврат'),
)

ORDER_ONE_C_NEW = 1
ORDER_ONE_C_TRANSFERRED_TO_ASSEMBLY = 2
ORDER_ONE_C_CONFIRMED_WAREHOUSE = 3
ORDER_ONE_C_ASSEMBLY_PREPARE = 4
ORDER_ONE_C_SHIPPED = 5
ORDER_ONE_C_DELIVERED = 6
ORDER_ONE_C_PARTIALLY_DELIVERED = 7
ORDER_ONE_C_DISBANDED = 8
ORDER_ONE_C_CONSOLIDATED = 9
ORDER_ONE_C_ABANDONED = 10
ORDER_ONE_C_UNDELIVERED = 11
ORDER_ONE_C_DELETED = 12

ORDER_STATUSES_ONE_C = (
    (ORDER_ONE_C_NEW, "Создан"),
    (ORDER_ONE_C_TRANSFERRED_TO_ASSEMBLY, "Отдан на сборку"),
    (ORDER_ONE_C_CONFIRMED_WAREHOUSE, "Принят складом"),
    (ORDER_ONE_C_ASSEMBLY_PREPARE, "Подготовка к сборке"),
    (ORDER_ONE_C_SHIPPED, "Отгружен"),
    (ORDER_ONE_C_DELIVERED, "Доставлен"),
    (ORDER_ONE_C_PARTIALLY_DELIVERED, "Частично доставлен"),
    (ORDER_ONE_C_DISBANDED, "Расформирован"),
    (ORDER_ONE_C_CONSOLIDATED, "Консолидирован"),
    (ORDER_ONE_C_ABANDONED, "Отказной"),
    (ORDER_ONE_C_UNDELIVERED, "Не доставлен"),
    (ORDER_ONE_C_DELETED, "Удален"),
)

BONUS_ACT_WAS_GENERATED = 1
BONUS_ACT_TRANSFERRED = 2
BONUS_ACT_SIGNED = 3
BONUS_ACT_SAVED = 4
BONUS_PAID = 5
BONUS_ERROR = 6

BONUS_PAYMENT_STATUSES = (
    (BONUS_ACT_WAS_GENERATED, 'Акт сформирован в системе дистрибьютора'),
    (BONUS_ACT_TRANSFERRED, 'Акт передан на подписание'),
    (BONUS_ACT_SIGNED, 'Акт подписан аптечным учреждением'),
    (BONUS_ACT_SAVED, 'Выплата оформлена в системе дистрибьютора'),
    (BONUS_PAID, 'Выплачено'),
    (BONUS_ERROR, 'Ошибка'),
)

LEGAL_ENTITY_ACTUAL = 'ACTUAL'
LEGAL_ENTITY_NOT_ACTUAL = 'NOT_ACTUAL'

LEGAL_ENTITY_STATUSES = (
    (LEGAL_ENTITY_ACTUAL, 'Актуальный'),
    (LEGAL_ENTITY_NOT_ACTUAL, 'Не Актуальный'),
)

LEGAL_ENTITY_ONBOARDED_FORMED = 'FORMED'
LEGAL_ENTITY_ONBOARDED_IN_PROCESS = 'IN_PROCESS'
LEGAL_ENTITY_ONBOARDED_SIGNED = 'SIGNED'
LEGAL_ENTITY_ONBOARDED_ERROR = 'ERROR'
LEGAL_ENTITY_ONBOARDED_CANCELED = 'CANCELED'

LEGAL_ENTITY_ONBOARDED_STATUSES = (
    (LEGAL_ENTITY_ONBOARDED_FORMED, 'Сформированный'),
    (LEGAL_ENTITY_ONBOARDED_IN_PROCESS, 'В процессе'),
    (LEGAL_ENTITY_ONBOARDED_SIGNED, 'Подписанный'),
    (LEGAL_ENTITY_ONBOARDED_ERROR, 'Ошибка'),
    (LEGAL_ENTITY_ONBOARDED_CANCELED, 'Отменён'),
)

CONSUMER = 1
PRODUCER = 2

KAFKA_CLIENT_TYPE = (
    (CONSUMER, 'Consumer'),
    (PRODUCER, 'Producer'),
)

ORDER_DATA_KEY = 'ЗаказФЗ'
