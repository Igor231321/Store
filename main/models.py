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


class Slider(models.Model):
    title = models.CharField(_("Назва"), max_length=100, unique=True)
    short_description = models.CharField(_("Короткий опис"), max_length=255)
    image = models.ImageField(_("Зображення"), unique=True, upload_to="slides/")
    is_active = models.BooleanField(_("Активне?"))
    url = models.URLField(_("Посилання"))
    url_text = models.CharField(_("Текст кнопки"), max_length=50)
    order = models.PositiveIntegerField(_("Порядок"), default=0)

    class Meta:
        db_table = "slider"
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдери"
        ordering = ["-order"]

    def __str__(self):
        return f"{self.title} ({self.is_active})"
