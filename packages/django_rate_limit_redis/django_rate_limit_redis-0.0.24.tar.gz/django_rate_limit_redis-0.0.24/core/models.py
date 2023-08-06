from uuid import uuid4

from django.core.cache import cache
from django.db import models

from .consts import BONUS_PAYMENT_STATUSES
from .consts import KAFKA_CLIENT_TYPE
from .consts import LEGAL_ENTITY_ONBOARDED_STATUSES
from .consts import LEGAL_ENTITY_STATUSES
from .consts import NULLABLE
from .consts import ORDER_STATUSES
from .consts import ORDER_STATUSES_ONE_C

ATTRIBUTE_TYPE_CHOICES = (
    ('str', 'Строка'),
    ('int', 'Целое число'),
    ('float', 'Число с плавающей точкой'),
    ('bool', 'Булево'),
)


class SettingsModel(models.Model):

    attribute_name = models.CharField("Имя атрибута", max_length=100)
    attribute_value = models.CharField(
        "Значение атрибута",
        max_length=255,
        help_text='Для булева значения используется True/False'
    )
    attribute_type = models.CharField("Тип атрибута", choices=ATTRIBUTE_TYPE_CHOICES, max_length=255)

    def save(self, *args, **kwargs):
        cache.set(
            self.attribute_name,
            {
                'value': self.attribute_value,
                'type': self.attribute_type,
            }
        )
        super(SettingsModel, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'


class SendedModelMixin(models.Model):
    sended = models.BooleanField("Передан в ФармЗаказ", default=False)
    sended_at = models.DateTimeField("Время отправки в ФЗ", null=True)

    class Meta:
        abstract = True


class Store(SendedModelMixin):
    """
    Обязательные поля
    inn* ИНН юридического лица
    legalName* Название юридического лица
    region* Субъект федерации (регион). К примеру, Московская обл
    city* Город (Населённый пункт). К примеру, Дмитров г
    street* Улица. К примеру, им Константина Аверьянова мкр
    building* Номер дома, строение и т.п. К примеру, 3
    hasContract* Имеет ли аптека действующий контракт с дистрибьютором?
    isBlackList* Находится ли аптека в черном списке дистрибьютора (дебиторы и пр.)?
    paymentDelay* Размер отсрочки платежа для аптеки (в днях)
    extId* Уникальный идентификатор аптеки в системе дистрибьютора
    warehouses* Склады с которыми работает аптека (РК и полагаю делать будем мы)
    """

    alias_fields = {
        'storeInfoId': 'store_info_id',
        'inn': 'inn',
        'legalName': 'legal_name',
        'fiasId': 'fias_id',
        'fiasCode': 'fias_code',
        'federalDistrict': 'federal_district',
        'region': 'region',
        'regionalDistrict': 'regional_district',
        'city': 'city',
        'street': 'street',
        'building': 'building',
        'fullAddress': 'full_address',
        'hasContract': 'has_contract',
        'blackList': 'black_list',
        'payment_delay': 'payment_delay',
        'posExtId': 'pos_ext_id',
        'created': 'created',
        'sended': 'sended',
        'sended_at': 'sended_at',
        'created_at': 'created_at',
        'branch': 'branch',
        'warehouses': 'warehouses',
    }

    store_info_id = models.IntegerField(  # swagger: integer
        verbose_name='Код аптеки в системе дистрибьютора',
        null=True,
        blank=True,
    )
    inn = models.CharField(  # swagger: integer TODO это странно, на проверку! REQUIRED
        verbose_name='ИНН юридического лица',
        max_length=100,
    )
    legal_name = models.CharField(  # swagger: integer TODO это странно, на проверку! REQUIRED
        verbose_name='Название юридического лица',
        max_length=100,
    )
    fias_id = models.CharField(  # swagger: integer TODO это странно, на проверку! REQUIRED
        verbose_name='ФИАС аптеки - номер',
        help_text='К примеру, 77000000000000004960678',
        max_length=100,
        null=True,
        blank=True,
    )
    fias_code = models.CharField(  # swagger: integer TODO это странно, на проверку!
        verbose_name='ФИАС аптеки - код',
        help_text='К примеру, 9acd20fe-ac30-45bc-a254-d60aa9b0be4e',
        max_length=100,
        null=True,
        blank=True,
        # **NULLABLE,
    )
    federal_district = models.CharField(  # REQUIRED
        verbose_name='Федеральный округ',
        help_text='К примеру, Центральный',
        max_length=100,
        null=True,
        blank=True,
    )
    region = models.CharField(  # REQUIRED
        verbose_name='Регион.',
        help_text='К примеру, Московская обл',
        max_length=100,
        **NULLABLE,
    )
    regional_district = models.CharField(  # REQUIRED
        verbose_name='Субъект федерации (регион).',
        help_text='К примеру, Центральный',
        max_length=100,
        null=True,
        blank=True,
    )
    city = models.CharField(  # REQUIRED
        verbose_name='Город (Населённый пункт)',
        help_text='К примеру, Дмитров г',
        max_length=100
    )
    street = models.CharField(  # REQUIRED
        verbose_name='Улица',
        help_text='К примеру, им Константина Аверьянова мкр',
        max_length=100
    )
    building = models.CharField(  # REQUIRED TODO возможно это Primary Key, либо PK который берём из 1С
        verbose_name='Строение',
        help_text='дом 5',
        max_length=10
    )
    full_address = models.CharField(
        verbose_name='Полный адрес аптеки.',
        help_text='К примеру, Московская обл, Дмитровский р-н, Дмитров г, им Константина Аверьянова мкр, 3',
        max_length=300,
        **NULLABLE,
    )
    has_contract = models.BooleanField(
        default=False,
        verbose_name='Имеет ли аптека действующий контракт с дистрибьютором?')

    black_list = models.BooleanField(
        default=False,
        verbose_name='Находится ли аптека в черном списке дистрибьютора (дебиторы и пр.)?')

    payment_delay = models.PositiveIntegerField(
        default=0,
        verbose_name='Размер отсрочки платежа для аптеки (в днях)'
    )

    pos_ext_id = models.CharField(  # swagger string REQUIRED TODO какой наш уникальный идентификатор?
        verbose_name='Уникальный идентификатор аптеки в системе дистрибьютора.',
        max_length=100,
        unique=True,
    )

    created = models.DateTimeField(  # TODO другой тип может быть нужен здесь? DateField
        verbose_name='Дата создания записи в БД Фарм-Заказ.',
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField("Время создания", auto_now=True)

    branch = models.CharField("ИНН РК", null=True, blank=False, default=None, max_length=12)
    warehouses = models.CharField(
        max_length=500,
        verbose_name='Склады Пульса',
        help_text="Пример: [{'warehouseId': 103}]",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Аптека'
        verbose_name_plural = 'Аптеки'


class Residue(SendedModelMixin):
    alias_fields = {
        'GTIN': 'gtin',
        'series': 'series',
        'EAN13': 'ean13',
        'warehouseExtId': 'warehouse_ext_id',
        'quantity': 'quantity',
        'expirationDate': 'expiration_date',
        'extId': 'ext_id',
    }

    gtin = models.CharField(
        max_length=27,
        verbose_name='GTIN – код товарной единицы согласно стандарту GS1.',
        help_text=' Если для не существует GTIN, то указывается EAN-13 (для БАДов, косметики и пр). Формат - 14 цифр',
        **NULLABLE
    )
    series = models.CharField(
        max_length=50,
        verbose_name='Номер серии товара.',
        help_text='Указывается номер серии товара, '
                  'для которой явным образом указана дата производства '
                  'и дата истечения срока годности',
        **NULLABLE,
    )
    ean13 = models.CharField(
        max_length=13,
        verbose_name='Код EAN13',
    )
    warehouse_ext_id = models.CharField(  # swagger REQUIRED Это ВЕРОЯТНО PrimaryKey
        max_length=100,
        verbose_name='Уникальный идентификатор склада в системе дистрибьютора',
        # TODO какой наш уникальный идентификатор?
    )
    quantity = models.IntegerField(  # swagger REQUIRED
        verbose_name='Количество упаковок на складе дистрибьютора, доступное для заказа',
        help_text='За исключением товаров в резерве, в транзите и т.п.',
    )
    expiration_date = models.DateField(  # swagger REQUIRED TODO другой тип может быть нужен здесь?
        verbose_name='Дата окончания срока годности',
        null=True,  # TODO на момент 07.02.22 реалиазации Кафка-консьюмера не было значения от 1С
    )
    ext_id = models.CharField(
        verbose_name='ID остатка товара в системе дистрибьютора',
        max_length=100,
        default=uuid4,  # swagger REQUIRED Это ВЕРОЯТНО PrimaryKey # TODO какой наш уникальный идентификатор?
        primary_key=True,
    )

    nomenclature = models.CharField(
        verbose_name="Номенклатура",
        null=False,
        max_length=5,
    )

    uid_batch = models.CharField(
        verbose_name="Идентификатор группы остатков",
        max_length=100,
        null=True,  # TODO на момент 07.02.22 реалиазации Кафка-консьюмера не было значения от 1С
    )

    created_at = models.DateTimeField(  # swagger REQUIRED TODO другой тип может быть нужен здесь?
        verbose_name='Время создания записи',
        auto_now=True
    )

    rest_time = models.DateTimeField(
        verbose_name='Время среза остатков',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'


class ResidueHistory(SendedModelMixin):
    gtin = models.CharField(
        max_length=27,
        verbose_name='GTIN – код товарной единицы согласно стандарту GS1.',
        help_text=' Если для не существует GTIN, то указывается EAN-13 (для БАДов, косметики и пр). Формат - 14 цифр',
        **NULLABLE
    )
    series = models.CharField(
        max_length=50,
        verbose_name='Номер серии товара.',
        help_text='Указывается номер серии товара, '
                  'для которой явным образом указана дата производства '
                  'и дата истечения срока годности',
        **NULLABLE,
    )
    ean13 = models.CharField(
        max_length=13,
        verbose_name='Код EAN13',
    )
    warehouse_ext_id = models.CharField(  # swagger REQUIRED Это ВЕРОЯТНО PrimaryKey
        max_length=100,
        verbose_name='Уникальный идентификатор склада в системе дистрибьютора',
        # TODO какой наш уникальный идентификатор?
    )
    quantity = models.IntegerField(  # swagger REQUIRED
        verbose_name='Количество упаковок на складе дистрибьютора, доступное для заказа',
        help_text='За исключением товаров в резерве, в транзите и т.п.',
    )
    expiration_date = models.DateField(  # swagger REQUIRED TODO другой тип может быть нужен здесь?
        verbose_name='Дата окончания срока годности',
    )
    ext_id = models.CharField(
        verbose_name='ID остатка товара в системе дистрибьютора',
        max_length=100,
        default=uuid4,  # swagger REQUIRED Это ВЕРОЯТНО PrimaryKey # TODO какой наш уникальный идентификатор?
        primary_key=True,
    )

    nomenclature = models.CharField(
        verbose_name="Номенклатура",
        null=False,
        max_length=5,
    )

    uid_batch = models.CharField(
        verbose_name="Идентификатор группы остатков",
        max_length=100,
    )

    created_at = models.DateTimeField(  # swagger REQUIRED TODO другой тип может быть нужен здесь?
        verbose_name='Время создания записи',
        auto_now=True
    )

    rest_time = models.DateTimeField(
        verbose_name='Время среза остатков',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'История остатка'
        verbose_name_plural = 'История остатков'


class Order(models.Model):  # в swagger для данной модели нет REQUIRED полей. Проверить.
    alias_fields = {
        'orderId': 'order_id',
        'status': 'status',
        'StoreExtId': 'store_ext_id',
        'updated': 'updated',
        'created': 'created',
        'warehouseExtId': 'warehouse_ext_id',
        'totalSum': 'total_sum',
        'vatSum': 'vat_sum',
        'positions': 'positions',
        'count_positions': 'count_positions',
        'sended_to_one_c': 'sended_to_one_c',
        'sended_to_pz': 'sended_to_pz',
    }

    order_id = models.BigAutoField(
        primary_key=True,
        editable=True,
    )

    status = models.CharField(
        verbose_name='Статус заказа.',
        choices=ORDER_STATUSES,
        max_length=30,
    )

    store_ext_id = models.CharField(  # swagger string TODO странный тип, возможно FK
        verbose_name='id аптеки в системе дистрибьютора',
        max_length=50,
    )

    updated = models.DateTimeField(
        verbose_name='Время, когда заказ был обновлен в последний раз в системе Фарм-Заказ',
        **NULLABLE,
    )

    created = models.DateTimeField(
        verbose_name='Время, когда заказ был создан в системе ФармЗаказ',
        **NULLABLE,
    )

    warehouse_ext_id = models.CharField(  # TODO возможно другой тип.
        verbose_name='id склада в системе дистрибьютора',
        help_text='example: H0312',
        max_length=100,
    )

    total_sum = models.DecimalField(
        verbose_name='Сумма заказа (С НДС)',
        help_text='example: 5000.5',
        max_digits=10,
        decimal_places=2,
    )

    vat_sum = models.DecimalField(
        verbose_name='Сумма НДС',
        help_text='example: 500',
        max_digits=10,
        decimal_places=2,
    )

    document_number = models.CharField(
        verbose_name='Номер заказа в 1С',
        max_length=11,
        **NULLABLE,
    )

    count_positions = models.IntegerField(
        verbose_name='Количество позиций в заказе',
        blank=True,

    )

    sended_to_one_c = models.BooleanField(default=False)
    sended_to_pz = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Position(models.Model):
    alias_fields = {
        'order': 'order',
        'GTIN': 'gtin',
        'EAN13': 'ean13',
        'Series': 'series',
        'itemId': 'item_id',
        'quantity': 'quantity',
        'price': 'price',
        'vat': 'vat',
        'expirationDate': 'expiration_date',
        'extId': 'ext_id',
        'invoiceNum': 'invoice_num',
        'warehouseExtId': 'warehouse_ext_id',
        'positionId': 'position_id',
        'info_received': 'info_received'
    }

    order = models.ForeignKey(
        Order,
        related_name='positions',
        on_delete=models.CASCADE
    )

    gtin = models.CharField(
        max_length=14,
        verbose_name='GTIN – код товарной единицы согласно стандарту GS1.',
        help_text='Если для не существует GTIN, то указывается EAN-13 (для БАДов, косметики и пр). Формат - 14 цифр, '
                  'example: 05907529465615',
    )

    ean13 = models.CharField(
        max_length=13,
        verbose_name='Код EAN13',
        help_text='example: 5907529465615',
    )

    series = models.CharField(
        max_length=50,
        verbose_name='Номер серии товара.',
        help_text='Указывается номер серии товара, '
                  'для которой явным образом указана дата производства '
                  'и дата истечения срока годности, '
                  'example: 040721',
        **NULLABLE,
    )

    item_id = models.CharField(
        verbose_name='Порядковый id позиции в заказе. ',
        help_text='Возможны 2 и более позиции в одинаковым GTIN (товар по обычной цене и товар с акцией)',
        max_length=100,
        **NULLABLE,
    )

    quantity = models.PositiveIntegerField(
        verbose_name='Количество позиции в заказе (шт.)',
        help_text='example: 30',
    )

    price = models.DecimalField(
        verbose_name='Цена без НДС для позиции в заказе (одной штуки)',
        help_text='example: 130.3',
        max_digits=10,
        decimal_places=2,
    )

    vat = models.DecimalField(
        verbose_name='Сумма НДС на данную позицию (одну штуку)',
        help_text='example: 13',
        max_digits=10,
        decimal_places=2,
    )

    expiration_date = models.DateField(
        verbose_name='Дата конца срока годности',
        help_text='example: 2024-06-30',
    )

    ext_id = models.CharField(  # TODO другой тип возможно, ВЕРОЯТНО это вообще PrimaryKey
        verbose_name='id продукта позиции в системе дистрибьютора',
        help_text='example: 30',
        max_length=100,
    )

    invoice_num = models.CharField(
        verbose_name='Номер накладной в которой отправлена позиция',
        max_length=100,
        null=True,
        blank=True,
    )
    warehouse_ext_id = models.CharField(
        max_length=100,
        verbose_name='Уникальный идентификатор склада в системе дистрибьютора',
        null=True,
        blank=True,
    )

    position_id = models.CharField(
        verbose_name='Идентификатор позиции в закказе фармзаказа',
        max_length=100,
        blank=True,
    )

    info_received = models.BooleanField(
        'Строка подтверждена 1С?',
        default=False
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'


class Invoice(SendedModelMixin):
    alias_fields = {
        'orderExtId': 'order_ext_id',
        'invoiceNum': 'invoice_num',
        'accepted': 'accepted',
        'delivered': 'delivered',
        'created': 'created',
        'isAccept': 'is_accept',
        'storeExtId': 'store_ext_id',
        'skuExtId': 'sku_ext_id',
        'deliveredQuantity': 'delivered_quantity',
        'deliveredSum': 'delivered_sum',
        'sended': 'sended',
        'sended_at': 'sended_at',
        'warehouse_ext_id': 'warehouse_ext_id',
        'invoice_id': 'invoice_id',
    }

    order_ext_id = models.CharField(
        "Номер заказа",
        max_length=30,
    )

    invoice_num = models.CharField(
        "Номер накладной",
        max_length=30,
        editable=True,
    )

    accepted = models.DateTimeField("Дата получения накладной", auto_now=True)

    delivered = models.DateTimeField("Дата доставки товара", **NULLABLE)

    created = models.DateTimeField("Дата создания")

    is_accept = models.BooleanField(
        "Принята аптекой?",
        default=False,
        **NULLABLE,  # TODO на момент 07.02.22 реалиазации Кафка-консьюмера не было значения от 1С
    )

    store_ext_id = models.CharField(
        verbose_name='Код аптеки в системе дистрибьютора',
        max_length=50,
    )

    sku_ext_id = models.CharField(
        verbose_name='Код товара в системе дистрибьютора',
        help_text='example: 00001',
        max_length=100,
    )

    delivered_quantity = models.PositiveIntegerField(
        verbose_name='Количество доставленных упаковок товара (шт.)',
        help_text='example: 30',
    )

    delivered_sum = models.DecimalField(
        verbose_name='Стоимость доставленных упаковок товара (С НДС)',
        help_text='example: 5000.5',
        max_digits=10,
        decimal_places=2,
    )

    warehouse_ext_id = models.CharField(
        max_length=100,
        verbose_name='Уникальный идентификатор склада в системе дистрибьютора',
    )

    invoice_id = models.IntegerField(
        "Идентификатор накладной в ФЗ",
        **NULLABLE,
    )

    class Meta:
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'


class BonusPayment(models.Model):
    alias_fields = {
        'bonusId': 'bonus_id',
        'bonusPaymentStatus': 'bonus_payment_status',
        'statusDate': 'status_date',
        'comment': 'comment',
        'paymentOrder': 'payment_order',
        'extId': 'ext_id',
    }

    bonus_id = models.PositiveIntegerField(
        verbose_name='ID бонуса в системе Фарм-Заказ',
    )

    bonus_payment_status = models.PositiveSmallIntegerField(
        verbose_name='Статус выплаты бонусов',
        choices=BONUS_PAYMENT_STATUSES,
        **NULLABLE,
    )

    status_date = models.DateField(  # swagger REQUIRED. очень странно
        verbose_name='Дата обновления статуса',
        **NULLABLE,
    )

    comment = models.CharField(
        verbose_name='Комментарий',
        max_length=500,
        **NULLABLE,
    )

    payment_order = models.CharField(  # swaagger string TODO возможно ForeignKey
        verbose_name='Номер подтверждающего документа (платёжного поручения, кредит-ноты и пр.)',
        max_length=100,
        **NULLABLE,
    )

    ext_id = models.CharField(  # swagger string TODO другой тип возможно
        verbose_name='Внешний id выплаты',
        max_length=100,
    )

    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонусы'


# TODO не понял зачем BonusPaymentWithId


class Nomenclature(SendedModelMixin):
    gtin = models.CharField(null=True, blank=True, default=None, max_length=14)
    ean13 = models.CharField(null=True, blank=True, default=None, max_length=13)
    code = models.CharField(primary_key=True, null=False, blank=False, max_length=5)
    name = models.CharField(null=False, blank=False, max_length=255)
    comment = models.CharField(null=True, max_length=255)

    class Meta:
        verbose_name = "Номенклатура"
        verbose_name_plural = "Номенклатуры"

    def __str__(self):
        return self.name


class Branch(SendedModelMixin):
    inn = models.CharField("ИНН", null=True, blank=False, default=None, max_length=12, unique=True)
    kpp = models.CharField("КПП", null=True, blank=True, default=None, max_length=9, )
    name = models.CharField("Название филиала", max_length=255)
    address = models.CharField("Адрес филиала", null=False, blank=False, max_length=255)
    created_at = models.DateTimeField("Время создания", auto_now=True)
    warehouse_id = models.PositiveIntegerField(verbose_name='Id в системе ФЗ', help_text='example: 30', null=True)
    ext_data = models.JSONField(null=True, blank=True, default=dict)
    guid = models.UUIDField("GUID филиала", default=uuid4)
    target_topic_to_send = models.CharField("Название топика для отправки", max_length=255)

    abbreviation = models.CharField("Сокращенное название (Префикс)", max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"

    def __str__(self):
        return self.name


class OrderStatusMap(models.Model):
    status_one_c = models.SmallIntegerField(
        verbose_name='Статус заказа в 1С',
        choices=ORDER_STATUSES_ONE_C,
    )
    status_pharm_zakaz = models.CharField(
        verbose_name='Статус заказа в ФармЗаказ',
        choices=ORDER_STATUSES,
        max_length=30,
    )

    class Meta:
        verbose_name = "Соответствие статусов"
        verbose_name_plural = "Соответствие статусов"


class ErrorsRequest(models.Model):
    created_at = models.DateTimeField("Время получения ошибки", auto_now=True)
    error = models.CharField("Текст ошибки запроса", max_length=500)
    request = models.CharField("Запрос", max_length=500, null=True)
    status_code = models.CharField("Код ответа", max_length=20, null=True)

    class Meta:
        verbose_name = "Ошибки запроса"
        verbose_name_plural = "Ошибки запросов"


class KafkaMsg(models.Model):
    created = models.DateTimeField("Время создания", auto_now=True)
    topic = models.CharField("Имя топика", max_length=120, )
    data_key = models.CharField("Ключ данных", max_length=120, )
    recipient = models.CharField("Получатель", max_length=120, )
    msg = models.JSONField(default=dict)
    dict_obj = models.JSONField(default=dict)

    class Meta:
        verbose_name = "Очередь сообщений"
        verbose_name_plural = "Очередь сообщений"


class LegalEntity(models.Model):
    pharm_zakaz_id = models.PositiveBigIntegerField(
        'Идентификатор на стороне ФармЗаказа',
        unique=True,
    )
    created = models.DateTimeField(
        verbose_name='Время, когда заказ был создан в системе ФармЗаказ',
        **NULLABLE,
    )
    inn = models.CharField(
        "ИНН",
        max_length=255,
        unique=True
    )
    opf = models.CharField(
        "Организационно правовая форма",
        max_length=255
    )
    legal_entity = models.CharField(
        "Название ЮЛ",
        max_length=255
    )
    address = models.CharField(
        "Юридический Адрес",
        max_length=300
    )
    full_name = models.CharField(
        "ФИО руководителя",
        max_length=255,
        **NULLABLE
    )
    position = models.CharField(
        "Должность руководителя",
        max_length=255,
        **NULLABLE
    )
    basis_authority = models.CharField(
        "Основание полномочий",
        max_length=300
    )
    bic = models.CharField(
        "БИК",
        max_length=27
    )
    bank_account = models.CharField(
        "Расчётный счёт",
        max_length=30
    )
    bank = models.CharField(
        "Название банка",
        max_length=300
    )
    kpp_juridical_person = models.CharField(
        "КПП организации",
        max_length=30,
        **NULLABLE
    )
    kpp_bank = models.CharField(
        "КПП банка",
        max_length=30,
        **NULLABLE
    )
    correspondent_account = models.CharField(
        "Корсчёт",
        max_length=30,
        default=None
    )
    status = models.CharField(
        'Статус запроса',
        choices=LEGAL_ENTITY_STATUSES,
        max_length=15,
        **NULLABLE,
    )
    updated = models.DateTimeField(
        verbose_name='Дата обновления запроса',
        **NULLABLE,
    )
    sended_to_1c = models.BooleanField(
        'Отправлено в 1C',
        default=False
    )

    class Meta:
        verbose_name = "Запрос юридических лиц"
        verbose_name_plural = "Запросы юридических лиц"

    def __str__(self):
        return self.legal_entity


class LegalEntityOnboarded(models.Model):
    pharm_zakaz_id = models.IntegerField(
        'Идентификатор на стороне ФАРМЗАКАЗА',
        **NULLABLE,
        unique=True,
    )
    inn = models.CharField(
        'ИНН',
        max_length=255,
    )
    contact_sign_date = models.DateTimeField(
        verbose_name='Дата заключения контракта',
    )
    status = models.CharField(
        'Статус запроса',
        choices=LEGAL_ENTITY_ONBOARDED_STATUSES,
        max_length=15,
    )
    status_updated = models.DateTimeField(
        verbose_name='Дата обновления статуса',
    )
    ext_id = models.CharField(
        'Идентификатор на стороне 1С',
        max_length=255,
        unique=True,
    )
    comment = models.CharField(
        'Комментарий',
        max_length=255
    )
    sended_to_pz = models.BooleanField(
        'Отправлено в ФАРМЗАКАЗ?',
        default=False,
    )
    sended_to_pz_at = models.DateTimeField(
        'Последняя дата отправки в ФАРМЗАКАЗ',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Одобренные запросы юридических лиц"
        verbose_name_plural = "Одобренные запросы юридических лиц"

    def __str__(self):
        return self.inn


class KafkaOffset(models.Model):
    created = models.DateTimeField("Время создания", auto_now=True)
    client_type = models.SmallIntegerField(
        verbose_name='Тип',
        choices=KAFKA_CLIENT_TYPE
    )
    topic = models.CharField("Имя топика", max_length=120, )
    offset = models.IntegerField("Смещение", )
    partition = models.IntegerField("Партиция", )

    class Meta:
        verbose_name = "Смещение сообщений кафки"
        verbose_name_plural = "Смещение сообщений кафки"


class DataHandlersMap(models.Model):
    data_handler = models.CharField("Имя обработчика", max_length=120, )
    topic = models.CharField("Имя топика", max_length=120, )

    class Meta:
        verbose_name = "Соответствие топика и обработчика"
        verbose_name_plural = "Соответствие топика и обработчика"


class ReconciliationResidue(models.Model):
    gtin = models.CharField(
        max_length=27,
        verbose_name='GTIN – код товарной единицы согласно стандарту GS1.',
        **NULLABLE
    )
    series = models.CharField(
        max_length=50,
        verbose_name='Номер серии товара.',
        **NULLABLE,
    )
    ean13 = models.CharField(
        max_length=13,
        verbose_name='Код EAN13',
    )
    warehouse_ext_id = models.CharField(
        max_length=100,
        verbose_name='Уникальный идентификатор склада в системе дистрибьютора',
    )
    quantity = models.IntegerField(
        verbose_name='Количество упаковок на складе дистрибьютора, доступное для заказа',
    )
    quantity_in_pz = models.IntegerField(
        verbose_name='Количество упаковок на складе дистрибьютора, доступное для заказа',
    )
    expiration_date = models.DateField(
        verbose_name='Дата окончания срока годности',
        null=True,
    )
    ext_id = models.CharField(
        verbose_name='ID остатка товара в системе дистрибьютора',
        max_length=100,
        default=uuid4,
    )

    nomenclature = models.CharField(
        verbose_name="Номенклатура",
        null=False,
        max_length=5,
    )

    uid_batch = models.CharField(
        verbose_name="Идентификатор группы остатков",
        max_length=100,
        null=True,
    )

    uid_reconciliation = models.CharField(
        verbose_name="Идентификатор группы сверки остатков",
        max_length=100,
        null=True,
    )

    created_at = models.DateTimeField(
        verbose_name='Время создания записи',
        auto_now_add=True
    )

    rest_time = models.DateTimeField(
        verbose_name='Время среза остатков',
        null=True,
        blank=True,
    )

    not_in_residue = models.BooleanField(
        verbose_name="Отсутствуют в нашей БД",
        default=False
    )

    not_in_pz = models.BooleanField(
        verbose_name="Отсутствуют в БД Фарм заказа",
        default=False
    )

    not_equal_quantity = models.BooleanField(
        verbose_name="Не сходится остаток",
        default=False
    )

    quantity_discrepancies = models.IntegerField(
        verbose_name='Количество упаковок расхождения',
        help_text='Количество упаковок большее или меньшее в сравнении нашей БД и Фарм заказа',
    )

    comment = models.CharField(
        verbose_name="Комментарий расхождения сверки",
        max_length=100,
        null=True,
    )

    class Meta:
        verbose_name = 'Сверка остатков'
        verbose_name_plural = 'Сверка остатков'
