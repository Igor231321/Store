from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Кастомний менеджер моделі користувача, в якому для автентифікації
    унікальним ідентифікатором є електронна пошта замість імені користувача.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Створює та зберігає користувача з вказаними електронною поштою та паролем.
        """
        if not email:
            raise ValueError("Потрібно вказати електронну пошту")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Створює та зберігає суперкористувача з вказаними електронною поштою та паролем.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперкористувач повинен мати is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперкористувач повинен мати is_superuser=True.")
        return self.create_user(email, password, **extra_fields)
