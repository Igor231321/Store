from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PROCESSING = "PR", "Обробляється"
        RECEIVED = "RC", "Отримано"
        CANCELLED = "CL", "Скасовано"

    user = models.ForeignKey(User, verbose_name=("Пользователь"), on_delete=models.CASCADE)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    status = models.CharField("Статус", choices=Status.choices, max_length=2, default=Status.PROCESSING)
    phone_number = models.CharField("Номер телефона", max_length=15)
    first_name = models.CharField("Ім'я", max_length=30)
    last_name = models.CharField("Фамілія", max_length=30)
    email = models.EmailField("Email", max_length=255)

    city = models.CharField("Місто", max_length=100)
    warehouse = models.CharField("Відділення НП", max_length=255)

    comment = models.TextField("Комментарий", blank=True, null=True)

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("-id",)

    def __str__(self):
        return f'Заказ №{self.pk})'
