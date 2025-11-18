from django.db import models


# Create your models here.
class AppVersion(models.Model):
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=50)
    date = models.DateField()
    description = models.TextField()
    app = models.ForeignKey(
        "apps.App", on_delete=models.CASCADE, related_name="versions"
    )

    def __str__(self):
        return f"{self.app.name} v{self.version}"
