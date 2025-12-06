# Create your views here.
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet

from installation.models import Installation
from installation.serializers import InstallationSerializer
from permissions import IsDeveloper


@extend_schema_view(
    create=extend_schema(
        summary="Create new installation",
        description="Create a new installation from  user",
    ),
    retrieve=extend_schema(
        summary="Retrieve installation",
        description="Retrieve installation",
    ),
)
class InstallationsViewSet(ModelViewSet):
    serializer_class = InstallationSerializer
    queryset = Installation.objects.all()

    def get_permissions(self):
        if self.action in {"retrieve"}:
            return [IsDeveloper()]
        return []


