from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from unidecode import unidecode

from product.managers import ProductQuerySet


class Brand(models.Model):
    name = models.CharField("Название", max_length=155, unique=True, null=True)
    slug = models.SlugField("SLUG_URL", max_length=155, unique=True, null=True)

    class Meta:
        db_table = "brand"
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField("Название", max_length=155, unique=True, null=True)
    rate = models.DecimalField("Курс",
                               decimal_places=2,
                               max_digits=4,
                               help_text="Максимум 4 цифри")

    class Meta:
        db_table = "currency"
        verbose_name = "Валюта"
        verbose_name_plural = "Валюти"

    def __str__(self):
        return f'{self.name} ({self.rate})'


class Category(MPTTModel):
    name = models.CharField("Назва", max_length=50, unique=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Батьківська категорія",
    )
    slug = models.SlugField("Слаг", max_length=50, unique=True)
    image = models.ImageField(upload_to="categories_images/")
    in_home_page = models.BooleanField("На головній сторінці?", default=False)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:category_detail", args=[self.slug])


class Attribute(models.Model):
    name = models.CharField("Название", max_length=50, unique=True, null=True)
    slug = models.SlugField("SLUG_URL", max_length=50, unique=True, null=True)

    class Meta:
        db_table = "attribute"
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибути"

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, null=True, verbose_name="Атрибут", related_name="values"
    )
    value = models.CharField("Значення", max_length=50, null=True)

    class Meta:
        db_table = "attribute_value"
        verbose_name = "Значення атрибута"
        verbose_name_plural = "Значення атрибутів"

    def __str__(self):
        attr = self.attribute.name if self.attribute else "Без атрибута"
        val = self.value or "Без значення"
        return f"{attr}: {val}"


class Product(models.Model):
    name = models.CharField("Название", max_length=155, unique=True, null=True)
    slug = models.SlugField("SLUG_URL", max_length=155, unique=True, null=True)
    description = models.TextField("Опис", null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категорія",
        related_name="products",
    )
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name="Бренд")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name="Валюта", blank=True, null=True)
    discount = models.DecimalField("Знижка у %", max_digits=10, decimal_places=2, blank=True, null=True)
    in_home_page = models.BooleanField("На головній сторінці?", default=False)

    class Meta:
        db_table = "product"
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:detail", kwargs={"slug": self.slug})

    objects = ProductQuerySet().as_manager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def display_price(self):
        if self.min_price_before_discount != self.max_price_before_discount:
            return f"{round(self.min_price_before_discount, 2)} грн. – {round(self.max_price_before_discount, 2)} грн."
        else:
            return f"{round(self.min_price_before_discount, 2)} грн."

    def display_price_with_discount(self):
        if self.min_price_after_discount != self.max_price_after_discount:
            return f"{round(self.min_price_after_discount, 2)} грн. – {round(self.max_price_after_discount, 2)} грн."
        else:
            return f"{round(self.min_price_after_discount, 2)} грн."


class ProductVariation(models.Model):
    class StatusTextChoices(models.TextChoices):
        IN_STOCK = "IN_STOCK", "В наличии"
        OUT_OF_STOCK = "OUT_OF_STOCK", "Нету в наличии"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variations",
        verbose_name="Товар",
    )
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Атрибут",
    )
    price = models.DecimalField("Ціна", max_digits=10, decimal_places=2)
    image = models.ImageField(
        "Зображення", upload_to="product_images/", blank=True, null=True
    )
    article = models.CharField("Артикул", max_length=255, unique=True)
    quantity = models.PositiveIntegerField("Кількість товару", default=0)
    status = models.CharField("Статус", choices=StatusTextChoices)

    class Meta:
        db_table = "product_variations"
        verbose_name = "Варіації товару"
        verbose_name_plural = "Варіації товару"
        ordering = ["price"]
        indexes = [
            models.Index(fields=["article"])
        ]

    def get_price(self):
        if self.product.currency:
            return round(self.product.currency.rate * self.price, 2)
        return self.price

    def get_price_with_discount(self):
        price = self.get_price()
        if self.product.discount:
            price = round(price - price * self.product.discount / 100, 2)

        return price

    def __str__(self):
        return f"{self.product.name} (Артикул: {self.article}, {self.attribute_value}, {self.get_status_display()})"


class ProductCharacteristics(models.Model):
    product_variation = models.ForeignKey(
        "ProductVariation",
        on_delete=models.CASCADE,
        related_name="characteristics",
        verbose_name="Варіація товару",
    )
    name = models.CharField("Название", max_length=155, null=True)
    value = models.CharField("Значення", max_length=50, null=True)

    class Meta:
        db_table = "product_characteristics"
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class Review(models.Model):
    product_variation = models.ForeignKey(to=ProductVariation, on_delete=models.CASCADE, related_name="reviews",
                                          verbose_name=_("Варіація продукта"))
    first_name = models.CharField(_("Ім'я"), max_length=100)
    last_name = models.CharField(_("Фамілія"), max_length=100)
    comment = models.CharField(_("Коментар"), max_length=255)
    created_at = models.DateTimeField(_("Дата створення"), auto_now_add=True)
    rating = models.PositiveIntegerField(_("Рейтинг"),
                                         validators=[MaxValueValidator(5,
                                                                       message=_("Максимальна оцінка 5"))])
    advantages = models.CharField(_("Переваги"), max_length=255, blank=True)
    disadvantages = models.CharField(_("Недоліки"), max_length=255, blank=True)

    class Meta:
        db_table = "review"
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    def __str__(self):
        return self.comment


class InStockNotification(models.Model):
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, verbose_name=_("Варіація товару"))
    first_name = models.CharField(_("Ім'я"), max_length=100)
    last_name = models.CharField(_("Фамілія"), max_length=100)
    phone_number = models.CharField(_("Номер телефону"), max_length=20)
    is_notified = models.BooleanField("Сповіщено", default=False)
    created_at = models.DateTimeField(_("Дата створення"), auto_now_add=True)

    class Meta:
        db_table = "in_stock_notification"
        verbose_name = _("Запит на наявність")
        verbose_name_plural = _("Запити на наявність")

    def __str__(self):
        if self.is_notified:
            notified_result = _("Сповіщено")
        else:
            notified_result = _("Не сповіщено")
        return f"{self.first_name}, {self.last_name} ({self.phone_number}, {notified_result})"
