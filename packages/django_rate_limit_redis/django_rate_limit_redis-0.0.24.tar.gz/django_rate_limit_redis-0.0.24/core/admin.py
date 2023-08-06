from users.models import AppGroup

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.db import models
from django.forms import TextInput

from core.management.commands.kafka_producer import PHKafkaProducer
from core.models import Branch
from core.models import DataHandlersMap
from core.models import ErrorsRequest
from core.models import Invoice
from core.models import KafkaMsg
from core.models import KafkaOffset
from core.models import LegalEntity
from core.models import LegalEntityOnboarded
from core.models import Nomenclature
from core.models import Order
from core.models import OrderStatusMap
from core.models import Position
from core.models import ReconciliationResidue
from core.models import Residue
from core.models import ResidueHistory
from core.models import SettingsModel
from core.models import Store
from core.systems.pharmzakaz import PharmZakazSystem


class DisableDeleteAdminMixin:
    def get_actions(self, request):
        actions = super(DisableDeleteAdminMixin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions["delete_selected"]
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


class CustomUserAdmin(DisableDeleteAdminMixin, UserAdmin):
    pass


class CustomGroupAdmin(DisableDeleteAdminMixin, GroupAdmin):
    pass


admin.site.unregister(Group)
admin.site.register(AppGroup, CustomGroupAdmin)
admin.site.register(get_user_model(), CustomUserAdmin)


@admin.register(SettingsModel)
class SettingsModelAdmin(admin.ModelAdmin):
    list_display = (
        "attribute_name",
        "attribute_value",
        "attribute_type",
    )
    fields = (
        "attribute_name",
        "attribute_value",
        "attribute_type",
    )


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "abbreviation",
        "inn",
        "kpp",
        "target_topic_to_send",
        "address",
        "sended",
        "sended_at",
        "created_at",
        "warehouse_id",
        "ext_data",

    )

    def get_list_branches(modeladmin, request, queryset):
        PharmZakazSystem().get_warehouses()

    def create_branches(modeladmin, request, queryset):
        PharmZakazSystem().send_warehouses(qs=queryset)

    def update_branches(modeladmin, request, queryset):
        PharmZakazSystem().update_warehouses(qs=queryset)

    get_list_branches.short_description = "Загрузить информацию из ФЗ"
    create_branches.short_description = "Создать выбранные склады в ФЗ"
    update_branches.short_description = "Обновить выбранные склады в ФЗ"
    actions = [get_list_branches, create_branches, update_branches]

    search_fields = ("name", "abbreviation")


@admin.register(OrderStatusMap)
class OrderStatusMapAdmin(admin.ModelAdmin):
    list_display = (
        "status_one_c",
        "status_pharm_zakaz",
    )


class PositionAdminTabInline(admin.TabularInline):
    model = Position
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '11'})},
        models.DecimalField: {'widget': TextInput(attrs={'size': '8'})},
        # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'status',
        'store_ext_id',
        'updated',
        'created',
        'warehouse_ext_id',
        'total_sum',
        'vat_sum',
        'count_positions',

    )
    inlines = [
        PositionAdminTabInline,
    ]
    date_hierarchy = 'created'
    list_filter = ('status', 'warehouse_ext_id')
    search_fields = ("order_id", "status", 'warehouse_ext_id')

    def create_msg_send_to_kafka(modeladmin, request, queryset):
        order_ids = list(queryset.values_list('order_id', flat=True))
        PharmZakazSystem().save_msg_order_after_download(order_ids)

    def send_orders_to_pz(modeladmin, request, queryset):
        order_ids = list(queryset.values_list('order_id', flat=True))
        for order_id in order_ids:
            PharmZakazSystem().order_update(order_id)

    create_msg_send_to_kafka.short_description = "Сгенерировать сообщение для кафки"
    send_orders_to_pz.short_description = "Отправить ордер в ФармЗаказ"
    actions = [create_msg_send_to_kafka, send_orders_to_pz]


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = (
        "gtin",
        "ean13",
        "code",
        "name",
        "sended",
        "sended_at",
        "comment",
    )

    def send_selected_nomenclature(modeladmin, request, queryset):
        PharmZakazSystem().update_all_nomenclature(qs=queryset)

    send_selected_nomenclature.short_description = "Отправить выбранные номенклатуры"
    actions = [send_selected_nomenclature]
    search_fields = (
        "gtin",
        "ean13",
        "code",
        "name",
        "sended",
        "sended_at",
        "comment",
    )


@admin.register(ErrorsRequest)
class ErrorsRequestAdmin(admin.ModelAdmin):
    list_display = (
        "request",
        "created_at",
        "error"
    )


@admin.register(Residue)
class ResidueAdmin(admin.ModelAdmin):
    list_display = (
        'gtin',
        'series',
        'ean13',
        'warehouse_ext_id',
        'quantity',
        'expiration_date',
        'ext_id',
        'nomenclature',
        'uid_batch',
        'sended',
        'sended_at',
        'created_at',
    )

    def send_all_residue(modeladmin, request, queryset):
        PharmZakazSystem().update_all_residues_batch()

    def send_selected_residue(modeladmin, request, queryset):
        ean13_list = queryset.distinct('ean13').values_list('ean13', flat=True)
        PharmZakazSystem().update_all_residues_batch(ean13_list=ean13_list, update_diff=False)

    def reset_all_residue(modeladmin, request, queryset):
        PharmZakazSystem().reset_all_residue()

    send_selected_residue.short_description = "Отправить выбранные остатки"
    send_all_residue.short_description = "Отправить все остатки"
    reset_all_residue.short_description = "Обнулить все остатки в ФЗ"
    actions = [send_all_residue, reset_all_residue, send_selected_residue]


@admin.register(ResidueHistory)
class ResidueHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'gtin',
        'series',
        'ean13',
        'warehouse_ext_id',
        'quantity',
        'expiration_date',
        'ext_id',
        'nomenclature',
        'uid_batch',
        'sended',
        'sended_at',
        'created_at',
    )


@admin.register(ReconciliationResidue)
class ReconciliationResidueAdmin(admin.ModelAdmin):
    list_display = (
        'gtin',
        'series',
        'ean13',
        'warehouse_ext_id',
        'quantity',
        'quantity_in_pz',
        'expiration_date',
        'ext_id',
        'nomenclature',
        'uid_batch',
        'created_at',
        'rest_time',
        'not_in_residue',
        'not_in_pz',
        'not_equal_quantity',
        'quantity_discrepancies',
        'comment',
        'uid_reconciliation',
    )
    list_filter = (
        'created_at',
        'uid_reconciliation',
        'warehouse_ext_id',
        'not_in_residue',
        'not_in_pz',
        'not_equal_quantity',
    )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = (
        'store_info_id',
        'inn',
        'branch',
        'legal_name',
        # 'fias_id',
        # 'fias_code',
        'federal_district',
        'region',
        'regional_district',
        'city',
        'street',
        'building',
        'full_address',
        'has_contract',
        'black_list',
        'payment_delay',
        'pos_ext_id',
        'created',
        'sended',
        'sended_at',
        'created_at'
    )

    def send_selected_store(modeladmin, request, queryset):
        PharmZakazSystem().create_store(qs=queryset)

    def update_selected_store(modeladmin, request, queryset):
        PharmZakazSystem().update_all_store(qs=queryset)

    send_selected_store.short_description = "Создать выбранные аптеки"
    update_selected_store.short_description = "Обновить выбранные аптеки"
    actions = [send_selected_store, update_selected_store]
    search_fields = (
        "inn",
        "store_info_id",
        "full_address",
    )


@admin.register(KafkaMsg)
class KafkaMsgAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'data_key',
        'recipient',
        'dict_obj',
        'topic',
        'msg'
    )

    def send_msg_to_kafka(modeladmin, request, queryset):
        kafka = PHKafkaProducer()
        for obj in queryset:
            kafka.send(obj.topic, obj.msg, obj.data_key, obj.recipient, obj.dict_obj)
            obj.delete()

    send_msg_to_kafka.short_description = "Отправить сообщение в кафку"
    actions = [send_msg_to_kafka]


@admin.register(KafkaOffset)
class KafkaOffsetAdmin(admin.ModelAdmin):
    list_display = (
        'created',
        'client_type',
        'topic',
        'offset',
        'partition',
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_num',
        'order_ext_id',
        'invoice_id',
        'accepted',
        'delivered',
        'created',
        'is_accept',
        'store_ext_id',
        'sku_ext_id',
        'delivered_quantity',
        'delivered_sum',
        'sended',
        'sended_at',
        'warehouse_ext_id'
    )

    def create_invoice_to_pz(modeladmin, request, queryset):
        PharmZakazSystem().create_invoice(qs=queryset)

    def update_invoice_to_pz(modeladmin, request, queryset):
        PharmZakazSystem().update_invoice(qs=queryset)

    create_invoice_to_pz.short_description = "Создать накладную в ФармЗаказе"
    update_invoice_to_pz.short_description = "Обновить накладную в ФармЗаказе"
    actions = [create_invoice_to_pz, update_invoice_to_pz]


@admin.register(DataHandlersMap)
class DataHandlersMapAdmin(admin.ModelAdmin):
    list_display = (
        'data_handler',
        'topic',
    )


@admin.register(LegalEntity)
class LegalEntityAdmin(admin.ModelAdmin):
    list_display = (
        'inn',
        'opf',
        'legal_entity',
        'pharm_zakaz_id',
        'bic',
        'status',
        'sended_to_1c',
    )

    def send_msg_send_to_kafka(modeladmin, request, queryset):
        PharmZakazSystem().send_legal_entities_to_1C(entities=queryset)

    send_msg_send_to_kafka.short_description = "Отправить запрос в 1C"
    actions = [send_msg_send_to_kafka]


@admin.register(LegalEntityOnboarded)
class LegalEntityOnboardedAdmin(admin.ModelAdmin):
    list_display = (
        'inn',
        'pharm_zakaz_id',
        'status',
        'ext_id',
        'sended_to_pz',
        'comment',
    )

    def send_selected_onboarded_legal_entities_to_pz(modeladmin, request, queryset):
        PharmZakazSystem().send_onboarded_legal_entities(qs=queryset)

    send_selected_onboarded_legal_entities_to_pz.\
        short_description = "Отправить выбранные одобренные юр.лица в ФАРМЗАКАЗ"
    actions = [send_selected_onboarded_legal_entities_to_pz, ]
