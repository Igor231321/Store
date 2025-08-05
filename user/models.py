from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import UserManager


class User(AbstractUser):
    username = None

    email = models.EmailField("Email", unique=True)
    phone_number = models.CharField(
        "Номер телефону", max_length=20, unique=True
    )
    surname = models.CharField("По батьківськи", max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        full_name = f"{self.first_name} {self.surname}".strip()
        phone = f" | Телефон: {self.phone_number}" if self.phone_number else ""
        return f"{full_name or self.email}{phone}"
