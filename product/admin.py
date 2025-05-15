from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from product.models import (Attribute, AttributeValue, Brand, Category,
                            Product, ProductCharacteristics, ProductVariation)


class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 0
    autocomplete_fields = ("attribute_value",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    prepopulated_fields = {"slug": ["name"]}
    list_editable = ["category"]
    inlines = [ProductVariationInline]


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


@admin.register(ProductCharacteristics)
class ProductCharacteristicsAdmin(admin.ModelAdmin):
    list_display = ["name", "value", "product_variation"]
    exclude = ["slug"]
