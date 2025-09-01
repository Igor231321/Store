from django.contrib import admin
from unfold.admin import ModelAdmin

from integrations.models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(ModelAdmin):
    list_display = ["service", "user"]
