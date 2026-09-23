from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "phone",
                    "department",
                    "designation",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "email",
                    "role",
                    "phone",
                    "department",
                    "designation",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "role",
        "department",
        "designation",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "role",
        "department",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "username",
        "email",
        "phone",
        "department",
        "designation",
    )