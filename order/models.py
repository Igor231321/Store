from django.db import models

from product.models import ProductVariation
from user.models import User


class OrderItemQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(item.products_sum() for item in self)


class Order(models.Model):
    class Status(models.TextChoices):
        PROCESSING = "PR", "Обробляється"
        RECEIVED = "RC", "Отримано"
        ACCEPT = "AC", "Прийнято"
        CANCELLED = "CL", "Скасовано"
        SENT = "SN", "Відправлено"
        SHIPPED = "SP", "В дорозі"

    user = models.ForeignKey(
        User, verbose_name="Користувач", on_delete=models.CASCADE, blank=True, null=True
    )
    session_key = models.CharField("Сессия", max_length=32, blank=True, null=True)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    status = models.CharField(
        "Статус", choices=Status.choices, max_length=2, default=Status.PROCESSING
    )
    phone_number = models.CharField("Номер телефону", max_length=15)
    first_name = models.CharField("Ім'я", max_length=30)
    last_name = models.CharField("Прізвище", max_length=30)
    surname = models.CharField("По батькові", max_length=30)
    email = models.EmailField("Email", max_length=255, blank=True, null=True)

    city = models.CharField("Місто", max_length=100)
    warehouse = models.CharField("Відділення НП", max_length=255)

    comment = models.TextField("Коментар", blank=True, null=True)

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
