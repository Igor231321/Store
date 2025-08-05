from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin

from .models import Group, Page, Slider


class PageTabAdmin(TranslationInlineModelAdmin):
    model = Page
    prepopulated_fields = {"slug": ["title"]}
    extra = 1


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["title"]

    inlines = [PageTabAdmin]


@admin.register(Page)
class PageAdmin(TranslationAdmin):
    list_display = ["title", "content", "created"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Slider)
class PageAdmin(TranslationAdmin):
    list_display = ["title", "short_description", "order"]

