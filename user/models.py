from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import UserManager


class User(AbstractUser):
    username = None

    email = models.EmailField("Email", unique=True)
    phone_number = models.CharField(
        "Номер телефону", max_length=20, blank=True, null=True
    )
    surname = models.CharField("По батьківськи", max_length=50)
    city = models.CharField("Місто", max_length=100, blank=True, null=True)
    warehouse = models.CharField("Відділення НП", max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return self.email
