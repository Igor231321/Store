from django.db import models
from django.urls import reverse


class Color(models.Model):
    name = models.CharField("Цвет", unique=True)

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


class CategoryChild(models.Model):
    title = models.CharField("Название", max_length=255)
    slug = models.SlugField("SLUG_URL", max_length=255, unique=True)
    image = models.ImageField("Изображение", upload_to="category-child_images")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Категория"
    )

    class Meta:
        db_table = "category_child"
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField("Название", max_length=255, unique=True)
    description = models.TextField("Описание")
    slug = models.SlugField(
        "SLUG_URL", max_length=255, unique=True, blank=True, null=True
    )
    quantity = models.PositiveIntegerField("Количество товара", default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категорія",
        blank=True,
        null=True,
    )
    category_child = models.ForeignKey(
        CategoryChild,
        on_delete=models.CASCADE,
        verbose_name="Подкатегория",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "product"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product:detail", kwargs={"slug": self.slug})


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variations")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField(
        "Изображение", upload_to="product_images/", blank=True, null=True
    )
    article = models.CharField("Артикул", max_length=255, blank=True, null=True)

    class Meta:
        db_table = "product_variations"
        verbose_name = "Вариации товара"
        verbose_name = "Вариации товара"

    def __str__(self):
        return f"{self.product.title} - {self.color}"


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Атрибут", related_name="attributes"
    )
    name = models.CharField("Название атрибута", max_length=100)
    value = models.CharField("Значение", max_length=100)

    class Meta:
        db_table = "product_attribute"
        verbose_name = "Атрибут товара"
        verbose_name_plural = "Атрибуты товара"

    def __str__(self):
        return f"Товар ({self.product.title}), Аттрибут ({self.name} - {self.value})"
