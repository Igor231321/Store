from django.contrib import admin
from unfold.admin import ModelAdmin

from user.forms import UserCreationForm
from user.models import User


class UserAdmin(ModelAdmin):
    add_form = UserCreationForm
    model = User

    list_display = ["email", "is_staff"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "surname",
                    "phone_number",
                )
            },
        ),
        (
            "Дозволи",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("tab",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    ordering = ("email",)


admin.site.register(User, UserAdmin)
