from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class AbstractNamedModel(models.Model):
    name = models.CharField("Название", max_length=155, unique=True)
    slug = models.SlugField("SLUG_URL", max_length=155, unique=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Brand(AbstractNamedModel):
    class Meta:
        db_table = "brand"
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Category(MPTTModel):
    name = models.CharField("Название", max_length=50, unique=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская категория",
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Attribute(AbstractNamedModel):
    class Meta:
        db_table = "attribute"
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"


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
        return f"{self.attribute.name} - {self.value}"


class Product(AbstractNamedModel):
    description = models.TextField("Описание")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категорія",
        related_name="products"
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        db_table = "product"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:detail", kwargs={"slug": self.slug})


class ProductVariation(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variations"
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Атрибут",
    )
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField(
        "Изображение", upload_to="product_images/", blank=True, null=True
    )
    article = models.CharField("Артикул", max_length=255)
    quantity = models.PositiveIntegerField("Количество товара", default=0)

    class Meta:
        db_table = "product_variations"
        verbose_name = "Вариации товара"
        verbose_name_plural = "Вариации товара"
        ordering = ["price"]

    def __str__(self):
        return f"{self.product.name} - {self.article}"


class ProductCharacteristics(AbstractNamedModel):
    product_variation = models.ForeignKey("ProductVariation", on_delete=models.CASCADE, related_name="characteristics")
    value = models.CharField("Значение", max_length=50)

    class Meta:
        db_table = "product_characteristics"
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"
