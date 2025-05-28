from django.db import models

from product.models import ProductVariation
from user.models import User


class CartQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(cart.products_sum() for cart in self)

    def total_quantity(self):
        return self.aggregate(total=models.Sum("quantity"))["total"] or 0


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач", blank=True, null=True)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField("Кількість", default=1)
    session_key = models.CharField("Сессия пользователя", max_length=32, blank=True, null=True)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)

    class Meta:
        db_table = "cart"
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"
        ordering = ("-id",)

    objects = CartQuerySet().as_manager()

    def __str__(self):
        return f"Кошик для {self.user.get_full_name()}: {self.product_variation.product.name} (x{self.quantity})"

    def products_sum(self):
        return self.quantity * self.product_variation.get_price_with_discount()
