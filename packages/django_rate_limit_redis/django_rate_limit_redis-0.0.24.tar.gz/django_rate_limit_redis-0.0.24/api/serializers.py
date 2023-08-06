from rest_framework import serializers

from core.models import BonusPayment
from core.models import Order
from core.models import Position
from core.models import Residue
from core.models import Store

# TODO READ ONLY ALL


class StoreSerializer(serializers.ModelSerializer):
    storeInfoId = serializers.CharField(source='store_info_id')
    inn = serializers.CharField()
    legalName = serializers.CharField(source='legal_name')
    fiasId = serializers.CharField(source='fias_id')
    fiasCode = serializers.CharField(source='fias_code')
    federalDistrict = serializers.CharField(source='federal_district')
    region = serializers.CharField()
    regionalDistrict = serializers.CharField(source='regional_district')
    city = serializers.CharField()
    street = serializers.CharField()
    building = serializers.CharField()
    fullAddress = serializers.CharField(source='full_address')
    hasContract = serializers.BooleanField(source='has_contract')
    blackList = serializers.BooleanField(source='black_list')
    payment_delay = serializers.CharField()
    posExtId = serializers.CharField(source='pos_ext_id')
    created = serializers.DateTimeField()

    class Meta:
        model = Store
        exclude_fields = [value for key, value in model.alias_fields.items() if key != value]
        exclude_fields.append('id')
        exclude = (exclude_fields)


class PositionSerializer(serializers.ModelSerializer):
    order = serializers.CharField()
    GTIN = serializers.CharField(source='gtin')
    EAN13 = serializers.CharField(source='ean13')
    Series = serializers.CharField(source='series')
    itemId = serializers.CharField(source='item_id')
    quantity = serializers.CharField()
    price = serializers.CharField()
    vat = serializers.CharField()
    expirationDate = serializers.DateField(source='expiration_date')
    extId = serializers.CharField(source='ext_id')
    invoiceNum = serializers.CharField(source='invoice_num')

    class Meta:
        model = Position
        exclude_fields = [value for key, value in model.alias_fields.items() if key != value]
        exclude_fields.append('id')
        exclude = (exclude_fields)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {k: v for k, v in data.items() if v is not None}


class OrderSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)

    orderId = serializers.CharField(source='order_id')
    status = serializers.CharField()
    StoreExtId = serializers.CharField(source='store_ext_id')
    updated = serializers.DateTimeField()
    created = serializers.DateTimeField()
    warehouseExtId = serializers.CharField(source='warehouse_ext_id')
    totalSum = serializers.CharField(source='total_sum')
    vatSum = serializers.CharField(source='vat_sum')

    class Meta:
        model = Order
        exclude_fields = [value for key, value in model.alias_fields.items() if key != value]
        exclude_fields.append('document_number')
        exclude = (exclude_fields)


class BonusSerializer(serializers.ModelSerializer):
    bonusId = serializers.CharField(source='bonus_id')
    bonusPaymentStatus = serializers.CharField(source='bonus_payment_status')
    statusDate = serializers.DateField(source='status_date')
    comment = serializers.CharField()
    paymentOrder = serializers.CharField(source='payment_order')
    extId = serializers.CharField(source='ext_id')

    class Meta:
        model = BonusPayment
        exclude_fields = [value for key, value in model.alias_fields.items() if key != value]
        exclude_fields.append('id')
        exclude = (exclude_fields)


class ResidueSerializer(serializers.ModelSerializer):
    GTIN = serializers.CharField(source='gtin')
    series = serializers.CharField()
    EAN13 = serializers.CharField(source='ean13')
    warehouseExtId = serializers.CharField(source='warehouse_ext_id')
    quantity = serializers.CharField()
    expirationDate = serializers.DateField(source='expiration_date')
    extId = serializers.CharField(source='ext_id')
    skuExtId = serializers.CharField(source='nomenclature')

    class Meta:
        model = Residue
        exclude_fields = [value for key, value in model.alias_fields.items() if key != value]
        exclude_fields.append('nomenclature')
        exclude_fields.append('uid_batch')
        exclude_fields.append('created_at')
        exclude = (exclude_fields)
