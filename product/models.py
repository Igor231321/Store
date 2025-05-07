from django.db import models
from django.urls import reverse


class Brand(models.Model):
    name = models.CharField("Название бренда", max_length=50)

    class Meta:
        db_table = "brand"
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField("Цвет", unique=True)
    slug = models.SlugField("SLUG_URL", unique=True, null=True)

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField("Название", max_length=255)
    slug = models.SlugField("SLUG_URL", max_length=255, unique=True)
    image = models.ImageField("Изображение", upload_to="category_images")

    class Meta:
        db_table = "category"
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField("Название", max_length=255, unique=True)
    description = models.TextField("Описание")
    slug = models.SlugField("SLUG_URL", max_length=255, unique=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категорія",
        blank=True,
        null=True,
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)

    characteristics = models.JSONField("Характеристики", blank=True, null=True)

    class Meta:
        db_table = "product"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product:detail", kwargs={"slug": self.slug})


class Attribute(models.Model):
    name = models.CharField("Название атрибута", max_length=50, unique=True)

    class Meta:
        db_table = "attribute"
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, null=True, verbose_name="Атрибут"
    )
    value = models.CharField("Значение", max_length=50)

    class Meta:
        db_table = "attribute_value"
        verbose_name = "Значение атрибута"
        verbose_name_plural = "Значения атрибутов"

    def __str__(self):
        return f'{self.attribute.name} - {self.value}'


class ProductVariation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variations"
    )
    attribute_value = models.ForeignKey(
        AttributeValue, on_delete=models.CASCADE, null=True, verbose_name="Атрибут"
    )
    # attribute_value = models.CharField("Значение атрибута", max_length=50, null=True)
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        related_name="variations",
        null=True,
        verbose_name="Цвет",
    )
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField(
        "Изображение", upload_to="product_images/", blank=True, null=True
    )
    article = models.CharField("Артикул", max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField("Количество товара", default=0)
    characteristics = models.JSONField("Характеристики", blank=True, null=True)

    class Meta:
        db_table = "product_variations"
        verbose_name = "Вариации товара"
        verbose_name_plural = "Вариации товара"

    def __str__(self):
        return f"{self.product.title} - {self.color}"
