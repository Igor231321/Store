from django import forms
from django.contrib import admin
from flat_json_widget.widgets import FlatJsonWidget
from mptt.admin import DraggableMPTTAdmin

from product.models import (
    Attribute,
    AttributeValue,
    Brand,
    Category,
    Color,
    Product,
    ProductVariation,
)


class ProductForm(forms.ModelForm):
    class Meta:
        widgets = {"characteristics": FlatJsonWidget}


class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 0
    autocomplete_fields = ("attribute_value",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ["name", "category"]
    prepopulated_fields = {"slug": ["name"]}

    inlines = [ProductVariationInline]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ["name"]}
    search_fields = ["name"]


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ["attribute__name", "value"]
    search_fields = ["attribute__name", "value"]


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    extra = 0


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    inlines = [AttributeValueInline]


admin.site.register(Brand)
admin.site.register(ProductVariation)

admin.site.register(Category, DraggableMPTTAdmin)
