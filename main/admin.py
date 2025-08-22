from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline

from .models import Group, Page, Slider


class PageTabAdmin(StackedInline):
    model = Page
    prepopulated_fields = {"slug": ["title"]}
    extra = 0
    tab = True


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ["title", "get_pages_name"]

    inlines = [PageTabAdmin]

    def get_pages_name(self, obj):
        return [page.title for page in obj.pages.all()]


@admin.register(Page)
class PageAdmin(ModelAdmin):
    list_display = ["title", "content", "created"]
    prepopulated_fields = {"slug": ["title"]}


@admin.register(Slider)
class SlideAdmin(ModelAdmin):
    list_display = ["title", "short_description", "url_text", "order", "is_active"]
    list_editable = ["order", "is_active"]
