from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from order.models import Country, Order, OrderItem, Warehouse


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    tab = True


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ["reference", "status", "user", "delivery_method"]
    list_editable = ["status"]
    empty_value_display = 'Не вказано'
    readonly_fields = "created_at",

    fieldsets = [
        ("Дані корустувача",
         {
             "classes": ["tab"],
             "fields": ["user", "session_key", "first_name", "last_name", "surname", "phone_number", "email"]
         }),
        ("Деталі замовлення",
         {
             "classes": ["tab"],
             'fields': ['status', 'paid', "reference", 'delivery_method', 'np_country', 'np_warehouse', 'np_terminal',
                        'ukr_address', 'ukr_post_code',
                        'meest_country', 'meest_warehouse', 'do_not_call', 'created_at', 'comment']})
    ]
    list_per_page = 20

    inlines = [OrderItemInline]


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ["description", "area_description", "country_type"]
    list_per_page = 20


@admin.register(Warehouse)
class WarehouseAdmin(ModelAdmin):
    list_display = ["description", "warehouse_type", "number"]
    search_fields = ["warehouse_type"]
    list_per_page = 20
