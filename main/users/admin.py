# Register your models here.
from django.contrib import admin

from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "login", "type", "active", "created_at")
    list_display_links = ("id", "email", "login")
    list_filter = ("type", "active")
    search_fields = ("email", "login")
    ordering = ("-id",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Основное", {
            "fields": (
                "email",
                "login",
                "type",
                "password",
                "active",
                "icon",
            )
        }),
        ("Организации", {
            "fields": ("organizations",)
        }),
        ("Системные", {
            "fields": ("created_at", "updated_at")
        }),
    )
