from django.contrib import admin
from unfold.admin import ModelAdmin

from cart.models import Cart


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ["product_variation", "quantity", "created_at"]
    readonly_fields = ["created_at"]
