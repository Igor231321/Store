from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from mptt.admin import DraggableMPTTAdmin

from product.mixins import ProductSlugMixin
from product.models import (Attribute, AttributeValue, Brand, Category,
                            Currency, Product, ProductCharacteristics,
                            ProductVariation, Review)


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


@admin.action(description="Позначити як 'В наявності'")
def set_status_in_stock(self, request, queryset):
    queryset.update(status=ProductVariation.StatusTextChoices.IN_STOCK)


@admin.action(description="Позначити як 'Нема в наявності'")
def set_status_out_in_stock(self, request, queryset):
    queryset.update(status=ProductVariation.StatusTextChoices.OUT_OF_STOCK)


@admin.register(ProductVariation)
class ProductVariationAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["product", "article", "attribute_value", "price", "status"]
    list_editable = ["price", "attribute_value", "status"]

    actions = [set_status_in_stock, set_status_out_in_stock]


@admin.register(Currency)
class CurrencyAdmin(ProductSlugMixin, admin.ModelAdmin):
    list_display = ["name", "rate"]
    list_display_links = ["name", "rate"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product_variation", "comment", "first_name", "last_name", "created_at"]
