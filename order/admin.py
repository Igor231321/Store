from django.contrib import admin

from order.models import Country, Order, OrderItem, Warehouse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "user", "country"]
    list_editable = ["status"]

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
