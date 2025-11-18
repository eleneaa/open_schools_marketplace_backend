from django.db import models


# Create your models here.
class Manifest(models.Model):
    app = models.OneToOneField(
        "apps.App",
        on_delete=models.CASCADE,
        related_name="manifest",
        name="app_table_id",
    )
    app_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    pages = models.JSONField()
    platform_version = models.JSONField()

    dir = models.CharField(
        max_length=10,
        choices=[("ltr", "Ltr"), ("rtl", "Rtl"), ("auto", "Auto")],
        default="auto",
    )
    lang = models.CharField(max_length=10, blank=True, default="")
    short_name = models.CharField(max_length=255, blank=True, default="")
    description = models.TextField(blank=True, default="")
    color_scheme = models.CharField(
        max_length=10,
        choices=[("dark", "Dark"), ("light", "Light"), ("auto", "Auto")],
        blank=True,
        default="",
    )

    version = models.JSONField(default=dict)

    icons = models.JSONField(default=list)
    device_type = models.JSONField(default=list)
    req_permissions = models.JSONField(default=list)
    widgets = models.JSONField(default=list)

    window = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Manifest for {self.name}"
