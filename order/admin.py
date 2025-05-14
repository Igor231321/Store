from django.contrib import admin

from order.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "user", "city"]
    list_editable = ["status"]
