from modeltranslation.translator import TranslationOptions, register

from product.models import (Attribute, AttributeValue, Category, Product,
                            ProductCharacteristics)


@register(Product)
class ProductOptions(TranslationOptions):
    fields = ["name", "description"]


@register(Attribute)
class AttributeOptions(TranslationOptions):
    fields = ["name"]


@register(AttributeValue)
class AttributeValueOptions(TranslationOptions):
    fields = ["value"]


@register(ProductCharacteristics)
class ProductCharacteristicsOptions(TranslationOptions):
    fields = ["name", "value"]


@register(Category)
class CategoryOptions(TranslationOptions):
    fields = ['name']
