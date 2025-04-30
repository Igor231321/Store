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


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ["name", "value"]


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "slug", "quantity"]
    prepopulated_fields = {"slug": ["title"]}

    inlines = [ProductVariationInline, ProductAttributeInline]


admin.site.register(ProductVariation)
admin.site.register(Color)
