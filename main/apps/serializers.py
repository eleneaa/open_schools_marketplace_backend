from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from app_version.models import AppVersion
from app_version.serializers import AppVersionSerializer
from apps.models import App
from config.serializers import CategorySerializer


class AppSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    latest_published_version = serializers.SerializerMethodField()

    @extend_schema_field(AppVersionSerializer)
    def get_latest_published_version(self, obj: App):
        latest_version = AppVersion.objects.filter(app=obj).order_by("-date").first()
        if latest_version:
            return AppVersionSerializer(latest_version).data
        return None

    class Meta:
        model = App
        fields = "__all__"
