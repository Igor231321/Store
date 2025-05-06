from django import forms
from django.contrib import admin
from flat_json_widget.widgets import FlatJsonWidget

from product.models import (Attribute, Brand, Category, Color, Product,
                            ProductVariation)


class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 0


class ProductForm(forms.ModelForm):
    class Meta:
        widgets = {"characteristics": FlatJsonWidget}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ("title", "category")
    prepopulated_fields = {"slug": ["title"]}

    inlines = [ProductVariationInline]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(Brand)
