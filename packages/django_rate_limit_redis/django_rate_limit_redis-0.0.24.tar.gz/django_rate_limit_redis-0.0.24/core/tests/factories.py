from datetime import datetime
import random

import factory
from factory import fuzzy
from faker import Faker

from core.consts import BONUS_PAYMENT_STATUSES
from core.consts import ORDER_STATUSES
from core.models import BonusPayment
from core.models import Order
from core.models import Position
from core.models import Residue
from core.models import Store

RANDOM_MAX = 99999999
DECIMAL_LOW = 1
DECIMAL_HIGH = 10000
fake = Faker('ru_RU')


def get_date(date):
    return datetime.strptime(
        date.strftime("%Y-%m-%d %H:%M:%S"),
        "%Y-%m-%d %H:%M:%S"
    ).astimezone()


class StoreFactory(factory.django.DjangoModelFactory):
    store_info_id = factory.LazyAttribute(lambda x: random.randrange(0, RANDOM_MAX))
    inn = '1234567890'
    legal_name = fake.company()
    fias_id = factory.Sequence(lambda n: f'77000000000000004960678{n}')
    fias_code = factory.Sequence(lambda n: f'9acd20fe-ac30-45bc-a254-d60aa9b0be4e{n}')
    federal_district = 'Центральный'
    region = 'Московская обл'
    regional_district = 'Дмитровский р-н'
    city = 'Дмитров г'
    street = 'им Константина Аверьянова мкр'
    building = factory.LazyAttribute(lambda x: random.randrange(0, RANDOM_MAX))
    full_address = fake.address()
    has_contract = bool(random.getrandbits(1))
    black_list = bool(random.getrandbits(1))
    payment_delay = factory.LazyAttribute(lambda x: random.randrange(0, RANDOM_MAX))
    pos_ext_id = factory.Sequence(lambda n: f'9acd20fe-ac30-45bc-a254-d60aa9b0be4e{n}')
    created = get_date(fake.date_object())

    class Meta:
        model = Store


class OrderFactory(factory.django.DjangoModelFactory):
    # orderId = Auto
    status = fuzzy.FuzzyChoice(ORDER_STATUSES, getter=lambda c: c[0])
    store_ext_id = factory.LazyAttribute(lambda x: random.randrange(0, RANDOM_MAX))
    updated = get_date(fake.date_object())
    created = get_date(fake.date_object())
    warehouse_ext_id = factory.Sequence(lambda n: f'H0312{n}')
    total_sum = fuzzy.FuzzyDecimal(DECIMAL_LOW, DECIMAL_HIGH, precision=2)
    vat_sum = fuzzy.FuzzyDecimal(DECIMAL_LOW, DECIMAL_HIGH, precision=2)
    count_positions = random.randrange(1, 10)

    @factory.post_generation
    def positions(self, create, extracted, **kwargs):
        return PositionFactory.create_batch(random.randrange(1, 10), order=self)

    class Meta:
        model = Order


class PositionFactory(factory.django.DjangoModelFactory):
    gtin = factory.Sequence(lambda n: f'057529561{n}')
    ean13 = factory.Sequence(lambda n: f'575265615{n}')
    series = factory.Sequence(lambda n: f'040721{n}')
    item_id = factory.Sequence(lambda n: f'9acd20fe-ac30-45bc-a254-d60aa9b0be4e{n}')
    quantity = factory.LazyAttribute(lambda x: random.randrange(1, RANDOM_MAX))
    price = fuzzy.FuzzyDecimal(DECIMAL_LOW, DECIMAL_HIGH, precision=2)
    vat = fuzzy.FuzzyDecimal(DECIMAL_LOW, DECIMAL_HIGH, precision=2)
    expiration_date = get_date(fake.date_object())
    ext_id = factory.Sequence(lambda n: f'9acd20fe-ac30-45bc-a254-d60aa9b0be4e{n}')
    invoice_num = factory.Sequence(lambda n: f'БРН40721{n}')

    class Meta:
        model = Position


class ResidueFactory(factory.django.DjangoModelFactory):
    gtin = factory.Sequence(lambda n: f'0579561{n}')
    series = factory.Sequence(lambda n: f'040721{n}')
    ean13 = '1234567890123'
    warehouse_ext_id = factory.Sequence(lambda n: f'9acd20fe-ac30-45bc-a254-d69b0be4e{n}')
    quantity = factory.LazyAttribute(lambda x: random.randrange(1, RANDOM_MAX))
    expiration_date = get_date(fake.date_object())
    ext_id = factory.Sequence(lambda n: f'9acd20fe-ac30-45bc-a254-d60aa9b0be4e{n}')
    nomenclature = '00008'

    class Meta:
        model = Residue


class BonusPaymentFactory(factory.django.DjangoModelFactory):
    bonus_id = factory.LazyAttribute(lambda x: random.randrange(1, RANDOM_MAX))
    bonus_payment_status = fuzzy.FuzzyChoice(BONUS_PAYMENT_STATUSES, getter=lambda c: c[0])
    status_date = get_date(fake.date_object())
    comment = factory.Sequence(lambda n: f'comment{n}')
    payment_order = factory.Sequence(lambda n: f'9acd20fe-ac30-45bc-a254-d69b0be4e{n}')
    ext_id = factory.Sequence(lambda n: f'9acd20fe-ac30-45bc-a254-d69b0be4e{n}')

    class Meta:
        model = BonusPayment
