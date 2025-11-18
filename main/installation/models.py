from django.db import models

# Create your models here.


class Installation(models.Model):
    app = models.ForeignKey(
        "apps.App", on_delete=models.CASCADE, related_name="installations"
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="installations",
    )
    installed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["app", "organization"]

    def __str__(self):
        return f"{self.app.name} in {self.organization.name}"
