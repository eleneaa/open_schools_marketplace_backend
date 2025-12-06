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
    config = models.ForeignKey("config.Config", on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    installed_by = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ["app", "organization"]

    def __str__(self):
        return f"{self.app.name} in {self.organization.name}"
