# Create your views here.
from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet

from apps.filtersets import AppFilterset
from apps.models import App
from apps.serializers import AppSerializer
from paginators import CustomPaginator


class AppViewSet(ModelViewSet):
    queryset = App.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AppFilterset
    pagination_class = CustomPaginator
    serializer_class = AppSerializer
