from rest_framework import serializers

from app_version.models import AppVersion


class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVersion
        exclude = ["app"]
