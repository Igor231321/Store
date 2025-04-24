from django.contrib import admin

from product.models import Category, CategoryChild, Product, ProductAttribute


@admin.register(CategoryChild)
class CategoryChildAdmin(admin.ModelAdmin):
    list_display = ["title"]
    prepopulated_fields = {"slug": ["title"]}


class CategoryChildInline(admin.StackedInline):
    model = CategoryChild
    extra = 1
    prepopulated_fields = {"slug": ["title"]}


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
    list_display = ["title", "price", "description", "article", "slug", "quantity"]
    prepopulated_fields = {"slug": ["title"]}

    inlines = [ProductAttributeInline]
