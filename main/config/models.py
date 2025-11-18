from django.db import models


# Create your models here.
class Config(models.Model):
    app = models.ForeignKey(
        "apps.App", on_delete=models.CASCADE, related_name="configs"
    )
    data = models.JSONField()  # json данных конфигурации

    def __str__(self):
        return f"Config for {self.app.name}"
