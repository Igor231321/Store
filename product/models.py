from django.db import models


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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        db_table = "category_child"
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField("Название", max_length=255, unique=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Изображение", upload_to="product_images/")
    description = models.TextField("Описание")
    article = models.CharField("Артикул", max_length=255)
    slug = models.SlugField("SLUG_URL", max_length=255, unique=True)
    quantity = models.PositiveIntegerField("Количество товара", default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    category_child = models.ForeignKey(CategoryChild, on_delete=models.CASCADE, verbose_name="Подкатегория")

    class Meta:
        db_table = "product"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Атрибут")
    name = models.CharField("Название атрибута", max_length=100)
    value = models.CharField("Значение", max_length=100)

    class Meta:
        db_table = "product_attribute"
        verbose_name = "Атрибут товара"
        verbose_name_plural = "Атрибуты товара"

    def __str__(self):
        return f"Товар ({self.product.title}), Аттрибут ({self.name} - {self.value})"
