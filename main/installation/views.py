# Create your views here.
from rest_framework.viewsets import ModelViewSet

from installation.models import Installation
from installation.serializers import InstallationSerializer
from permissions import IsDeveloper


class InstallationsViewSet(ModelViewSet):
    serializer_class = InstallationSerializer
    queryset = Installation.objects.all()

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsDeveloper()]
        return []
