from django.contrib import admin

from .models import Group, Page


class PageTabAdmin(admin.StackedInline):
    model = Page
    prepopulated_fields = {"slug": ["title"]}
    extra = 1


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["title"]

    inlines = [PageTabAdmin]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "content", "created"]
    prepopulated_fields = {"slug": ["title"]}
