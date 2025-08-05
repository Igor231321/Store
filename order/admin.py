from django.contrib import admin

from order.models import Country, Order, OrderItem, Warehouse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["reference", "status", "user", "delivery_method", "paid"]
    list_editable = ["status"]
    empty_value_display = 'Не вказано'
    readonly_fields = "created_at",

    fieldsets = [
        ("Дані корустувача",
         {
             "classes": ["wide"],
             "fields": ["user", "session_key", "first_name", "last_name", "surname", "phone_number", "email"]
         }),
        ("Деталі замовлення",
         {
             "classes": ["collapse"],
             'fields': ['status', 'paid', "reference", 'delivery_method', 'np_country', 'np_warehouse', 'np_terminal',
                        'ukr_address', 'ukr_post_code',
                        'meest_country', 'meest_warehouse', 'do_not_call', 'created_at', 'comment']})
    ]
    list_per_page = 20

    inlines = [OrderItemInline]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["description", "area_description", "country_type"]
    list_per_page = 20


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["description", "warehouse_type", "number"]
    search_fields = ["warehouse_type"]
    list_per_page = 20
