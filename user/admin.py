from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.forms import UserCreationForm
from user.models import User

# admin.site.register(User)


class UserAdmin(UserAdmin):
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
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
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
