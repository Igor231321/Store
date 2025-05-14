from django.contrib import admin

from order.models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "user", "city"]
    list_editable = ["status"]

    inlines = [OrderItemInline]
