from django.db import models


# Create your models here.
class Subscription(models.Model):
    SUBSCRIPTION_PERIODS = (
        ("1month", "1 Month"),
        ("3m", "3 Months"),
        ("6m", "6 Months"),
        ("1year", "1 Year"),
    )

    STATUS_CHOICES = (
        ("active", "Active"),
        ("disable", "Disable"),
    )

    organization = models.ForeignKey(
        "organizations.Organization", on_delete=models.CASCADE, related_name="payments"
    )
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="payments"
    )
    payment_period = models.CharField(max_length=10, choices=SUBSCRIPTION_PERIODS)
    last_time_pay = models.DateTimeField()
    active = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    app = models.ForeignKey(
        "apps.App", on_delete=models.CASCADE, related_name="payments"
    )

    def __str__(self):
        return f"Subscription for {self.app.name} by {self.organization.name}"
