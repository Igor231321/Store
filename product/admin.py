from django.contrib import admin
from modeltranslation.admin import (TabbedTranslationAdmin,
                                    TranslationTabularInline)
from mptt.admin import DraggableMPTTAdmin
from unfold.admin import ModelAdmin, StackedInline, TabularInline
from unfold.contrib.filters.admin import BooleanRadioFilter

from product.models import (Attribute, AttributeValue, Brand, Category,
                            Currency, InStockNotification, Product,
                            ProductCharacteristics, ProductVariation, Review)


@admin.action(description="Відобразити на головній сторінці")
def in_home_page_true(self, request, queryset):
    queryset.update(in_home_page=True)


@admin.action(description="Не відображати на головній сторінці")
def in_home_page_false(self, request, queryset):
    queryset.update(in_home_page=False)


@admin.action(description="Позначити як 'В наявності'")
def set_status_in_stock(self, request, queryset):
    queryset.update(status=ProductVariation.StatusTextChoices.IN_STOCK)


@admin.action(description="Позначити як 'Нема в наявності'")
def set_status_out_in_stock(self, request, queryset):
    queryset.update(status=ProductVariation.StatusTextChoices.OUT_OF_STOCK)


class ProductVariationInline(StackedInline):
    model = ProductVariation
    extra = 0
    autocomplete_fields = ("attribute_value",)
    tab = True


@admin.register(Product)
class ProductAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["name", "category", "discount", "in_home_page"]
    list_editable = ["category", "discount", "in_home_page"]
    search_fields = ["name", "category__name", "discount"]
    list_per_page = 30
    prepopulated_fields = {"slug": ["name"]}
    inlines = [ProductVariationInline]
    actions = [in_home_page_true, in_home_page_false]


@admin.register(AttributeValue)
class AttributeValueAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["attribute__name", "value"]
    search_fields = ["attribute__name", "value"]


class AttributeValueInline(TranslationTabularInline):
    model = AttributeValue
    extra = 0


@admin.register(Attribute)
class AttributeAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["name", "get_attribute_values"]
    search_fields = ["name"]

    inlines = [AttributeValueInline]

    def get_attribute_values(self, obj):
        return [item.value for item in obj.values.all()]

    get_attribute_values.short_description = "Значення атрибута"


class ProductCharacteristicsInline(TabularInline, TranslationTabularInline):
    model = ProductCharacteristics
    extra = 0
    tab = True


@admin.register(ProductCharacteristics)
class ProductCharacteristicsAdmin(ModelAdmin, TabbedTranslationAdmin):
    list_display = ["name", "value", "product_variation"]


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, ModelAdmin, TabbedTranslationAdmin):
    list_display = ["tree_actions", "indented_title", "name", "in_home_page"]
    prepopulated_fields = {"slug": ["name"]}
    actions = [in_home_page_true, in_home_page_false]


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(ProductVariation)
class ProductVariationAdmin(ModelAdmin):
    list_display = ["product", "article", "attribute_value", "price", "status"]
    list_editable = ["price", "attribute_value", "status"]

    actions = [set_status_in_stock, set_status_out_in_stock]
    inlines = [ProductCharacteristicsInline]


@admin.register(Currency)
class CurrencyAdmin(ModelAdmin):
    list_display = ["name", "rate"]
    list_display_links = ["name", "rate"]


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ["product_variation", "comment", "first_name", "last_name", "created_at", "rating"]
    list_filter = ["rating"]
    search_fields = ["product_variation__article", "product_variation__product__name", "rating"]
    readonly_fields = ["created_at"]


@admin.register(InStockNotification)
class InStockNotificationAdmin(ModelAdmin):
    list_display = ["product_variation", "first_name", "last_name", "phone_number", "created_at", "is_notified"]
    readonly_fields = ["created_at"]
    list_filter = [
        ("is_notified", BooleanRadioFilter)
    ]
    list_filter_submit = True
