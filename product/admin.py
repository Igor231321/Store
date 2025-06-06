from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from mptt.admin import DraggableMPTTAdmin

from product.mixins import ProductSlugMixin
from product.models import (Attribute, AttributeValue, Brand, Category,
                            Currency, Product, ProductCharacteristics,
                            ProductVariation)


class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 1
    autocomplete_fields = ("attribute_value",)


@admin.register(Product)
class ProductAdmin(ProductSlugMixin, TranslationAdmin):
    list_display = ["name", "category", "discount"]
    list_editable = ["category", "discount"]

    inlines = [ProductVariationInline]


@admin.register(AttributeValue)
class AttributeValueAdmin(ProductSlugMixin, TranslationAdmin):
    list_display = ["attribute__name", "value"]
    search_fields = ["attribute__name", "value"]


class AttributeValueInline(TranslationTabularInline):
    model = AttributeValue
    extra = 1


@admin.register(Attribute)
class AttributeAdmin(ProductSlugMixin, TranslationAdmin):
    list_display = ["name"]
    search_fields = ["name"]

    inlines = [AttributeValueInline]


@admin.register(ProductCharacteristics)
class ProductCharacteristicsAdmin(ProductSlugMixin, TranslationAdmin):
    list_display = ["name", "value", "product_variation"]


@admin.register(Category)
class CategoryAdmin(ProductSlugMixin, DraggableMPTTAdmin, TranslationAdmin):
    list_display = ["tree_actions", "indented_title", "name"]


@admin.register(Brand)
class BrandAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["name"]


@admin.register(ProductVariation)
class ProductVariationAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["product", "article", "attribute_value", "price"]
    list_editable = ["price", "attribute_value"]


@admin.register(Currency)
class CurrencyAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["name", "rate"]
    list_display_links = ["name", "rate"]
