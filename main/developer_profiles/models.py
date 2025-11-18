from django.db import models

# Create your models here.


class DeveloperProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="developer_profile"
    )

    def __str__(self):
        return f"Developer: {self.user.login}"
