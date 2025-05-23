from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from product.mixins import ProductSlugMixin
from product.models import (
    Attribute,
    AttributeValue,
    Brand,
    Category,
    Product,
    ProductCharacteristics,
    ProductVariation,
)


class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 0
    autocomplete_fields = ("attribute_value",)


@admin.register(Product)
class ProductAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["name", "category"]
    list_editable = ["category"]

    inlines = [ProductVariationInline]


@admin.register(AttributeValue)
class AttributeValueAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["attribute__name", "value"]
    search_fields = ["attribute__name", "value"]


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    extra = 0


@admin.register(Attribute)
class AttributeAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    inlines = [AttributeValueInline]


@admin.register(ProductCharacteristics)
class ProductCharacteristicsAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["name", "value", "product_variation"]


@admin.register(Category)
class CategoryAdmin(ProductSlugMixin, DraggableMPTTAdmin):
    list_display = ["tree_actions", "indented_title", "name"]


@admin.register(Brand)
class BrandAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["name"]


@admin.register(ProductVariation)
class ProductVariationAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["product", "article", "attribute_value", "price"]
    list_editable = ["price", "attribute_value"]
