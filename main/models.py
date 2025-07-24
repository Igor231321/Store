from django.db import models
from django.utils.translation import gettext_lazy as _


class Page(models.Model):
    title = models.CharField(_("Назва"), max_length=155)
    slug = models.SlugField("Слаг", max_length=155, unique=True)
    content = models.TextField(_("Контент сторінки"))
    created = models.DateTimeField(_("Дата створення"), auto_now_add=True)

    class Meta:
        db_table = "page"
        verbose_name = "Сторінка"
        verbose_name_plural = "Сторінки"

    def __str__(self):
        return self.title
