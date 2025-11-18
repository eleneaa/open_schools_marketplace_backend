from django.db import models

# Create your models here.

class App(models.Model):
    APP_TYPES = (
        ('internal', 'Internal'),
        ('external', 'External'),
    )

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending_review', 'Pending Review'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=APP_TYPES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    icon_url = models.URLField(blank=True)
    screenshots = models.JSONField(default=list, blank=True)  # список URL или путей к файлам
    developer = models.ForeignKey("developer_profiles.DeveloperProfile", on_delete=models.CASCADE, related_name='apps')
    category = models.ForeignKey("category.Category", on_delete=models.SET_NULL, null=True, related_name='apps')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

