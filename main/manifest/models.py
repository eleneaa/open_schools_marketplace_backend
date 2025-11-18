from django.db import models

# Create your models here.
class Manifest(models.Model):
    app = models.OneToOneField("apps.App", on_delete=models.CASCADE, related_name='manifest', name="app_table_id")
    icons = models.JSONField(default=list)  # список иконок
    name = models.CharField(max_length=255)
    app_id = models.IntegerField()
    ... # TODO добавить остальные поля манифеста

    def __str__(self):
        return f"Manifest for {self.name}"
