from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField("Номер телефону", max_length=20, blank=True, null=True)
    surname = models.CharField("По батьківськи", max_length=50)
    city = models.CharField("Місто", max_length=100, blank=True, null=True)
    warehouse = models.CharField("Відділення НП", max_length=255, blank=True, null=True)

    class Meta:
        db_table = "user"
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return f'{self.username}, {self.email}'
