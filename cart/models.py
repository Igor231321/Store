from django.contrib.auth.models import User
from django.db import models

from product.models import ProductVariation


class CartQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(cart.products_sum() for cart in self)


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField("Количество", default=0)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        db_table = "cart"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = "-id",

    objects = CartQuerySet().as_manager()

    def __str__(self):
        return (
            f"Корзина для {self.user.username}: {self.product_variation.product.title} (x{self.quantity})"
        )

    def products_sum(self):
        return self.quantity * self.product_variation.price
