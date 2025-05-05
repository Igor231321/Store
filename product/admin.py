from django.contrib import admin

from product.models import (Category, CategoryChild, Color, Product,
                            ProductAttribute, ProductVariation)


@admin.register(CategoryChild)
class CategoryChildAdmin(admin.ModelAdmin):
    list_display = ["title"]
    prepopulated_fields = {"slug": ["title"]}


class CategoryChildInline(admin.StackedInline):
    model = CategoryChild
    extra = 1
    prepopulated_fields = {"slug": ["title"]}


class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]
    prepopulated_fields = {"slug": ["title"]}
    inlines = [CategoryChildInline]


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "quantity"]
    prepopulated_fields = {"slug": ["title"]}

    inlines = [ProductVariationInline, ProductAttributeInline]


admin.site.register(ProductVariation)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"slug": ["name"]}
