from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field


class Group(models.Model):
    title = models.CharField(_("Назва"), max_length=50, unique=True)

    class Meta:
        db_table = "group"
        verbose_name = "Група"
        verbose_name_plural = "Групи"

    def __str__(self):
        return self.title


class Page(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="pages", verbose_name=_("Група"), null=True)
    title = models.CharField(_("Назва"), max_length=155, unique=True)
    slug = models.SlugField("URL", max_length=155, unique=True)
    content = CKEditor5Field(_("Контент сторінки"), config_name="extends")
    created = models.DateTimeField(_("Дата створення"), auto_now_add=True)

    class Meta:
        db_table = "page"
        verbose_name = "Сторінка"
        verbose_name_plural = "Сторінки"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:page_detail", args=[self.slug])
