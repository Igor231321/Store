from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from product.models import ProductVariation
from user.models import User


class OrderItemQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(item.products_sum() for item in self)


class Country(models.Model):
    description = models.CharField(max_length=50, db_index=True)
    area_description = models.CharField(max_length=50)
    country_type = models.CharField(max_length=36)
    ref = models.CharField(max_length=36)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "countries"
        verbose_name = "Населений пункт"
        verbose_name_plural = "Населені пункти"
        ordering = ["country_type"]

    def __str__(self):
        country_types = {
            "місто": "м.",
            "село": "с.",
            "селище міського типу": "смт.",
            "селище": 'c'
        }
        return f"{country_types[self.country_type]} {self.description} ({self.area_description} обл.)"


class Warehouse(models.Model):
    class WarehouseType(models.TextChoices):
        POST_OFFICE = "PO", "Поштове відділення"
        TERMINAL = "TR", "Поштомат"

    country = models.ForeignKey("Country", on_delete=models.CASCADE, related_name="warehouses")
    description = models.CharField(max_length=100)
    warehouse_type = models.CharField(max_length=2, choices=WarehouseType)
    number = models.IntegerField()

    class Meta:
        ordering = ["number"]
        db_table = "warehouses"
        verbose_name = "Відділення"
        verbose_name_plural = "Відділення"
        indexes = [
            models.Index(fields=["warehouse_type"])
        ]

    def __str__(self):
        return self.description


class Order(models.Model):
    class Status(models.TextChoices):
        PROCESSING = "PR", _("Обробляється")
        RECEIVED = "RC", _("Отримано")
        ACCEPT = "AC", _("Прийнято")
        CANCELLED = "CL", _("Скасовано")
        SENT = "SN", _("Відправлено")
        SHIPPED = "SP", _("В дорозі")

    class DeliveryMethod(models.TextChoices):
        NP_WAREHOUSE = "NP_WH", _("Відділення Нової пошти")
        NP_TERMINAL = "NP_TR", _("Поштомат Нової пошти")
        UKR_WAREHOUSE = "UKR_WH", _("Відділення Укрпошти")
        MEEST_WAREHOUSE = "MEEST_WH", _("Відділення Meest")

    user = models.ForeignKey(
        User, verbose_name="Користувач", on_delete=models.CASCADE, blank=True, null=True
    )
    session_key = models.CharField("Сессия", max_length=32, blank=True, null=True)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    status = models.CharField(
        "Статус", choices=Status, max_length=2, default=Status.PROCESSING
    )
    phone_number = models.CharField("Номер телефону", max_length=25)
    first_name = models.CharField("Ім'я", max_length=30)
    last_name = models.CharField("Прізвище", max_length=30)
    surname = models.CharField("По батькові", max_length=30)
    email = models.EmailField("Email", max_length=255, blank=True, null=True)
    np_country = models.CharField("Місто НП", max_length=100, blank=True, null=True)
    delivery_method = models.CharField("Спосіб доставки", max_length=50,
                                       choices=DeliveryMethod, default=DeliveryMethod.NP_WAREHOUSE)
    np_warehouse = models.CharField("Відділення НП", max_length=255, blank=True, null=True)
    np_terminal = models.CharField("Поштомат НП", max_length=255, blank=True, null=True)
    ukr_address = models.CharField("Адрес УКР", max_length=255, blank=True, null=True)
    ukr_post_code = models.IntegerField('Поштовий індекс УКР', blank=True, null=True,
                                        validators=[MinValueValidator(1),
                                                    MaxValueValidator(99999)])
    meest_country = models.CharField("Місто MEEST", max_length=100, blank=True, null=True)
    meest_warehouse = models.CharField("Відділення Meest", max_length=255, blank=True, null=True)
    comment = models.TextField("Коментар", blank=True, null=True)
    do_not_call = models.BooleanField("Не передзвонювати для підтвердження замовлення", default=False)

    class Meta:
        db_table = "order"
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ("-id",)

    def __str__(self):
        return f"Замовлення №{self.pk})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Замовлення", related_name="items"
    )
    product_variation = models.ForeignKey(
        ProductVariation, on_delete=models.CASCADE, verbose_name="Варіація товара"
    )
    quantity = models.PositiveIntegerField("Кількість", default=1)

    class Meta:
        db_table = "order_item"
        verbose_name = "Проданий товар"
        verbose_name_plural = "Продані товари"

    objects = OrderItemQuerySet.as_manager()

    def __str__(self):
        return self.product_variation.product.name

    def products_sum(self):
        return self.quantity * self.product_variation.get_price_with_discount()
