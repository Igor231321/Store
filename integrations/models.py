from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class ApiKey(models.Model):
    class ServiceChoices(models.TextChoices):
        NOVA_POST = "nova_post", _("Нова почта")
        WAYFORPAY = "wayforpay", _("Wayforpay")

    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="api_keys",
                             verbose_name=_("Користувач"))
    service = models.CharField(_("Сервіс"), max_length=20, choices=ServiceChoices)
    key = models.CharField(_("Ключ"), max_length=255)

    class Meta:
        db_table = "api_key"
        verbose_name = _("Ключ API")
        verbose_name_plural = _("Ключі API")
        unique_together = ("user", "service")

    def __str__(self):
        return f"{self.get_service_display()} — {self.user}"
