# Create your views here.
from django_filters import rest_framework as filters
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location="query",
                required=False,
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location="query",
                required=False,
            ),
            OpenApiParameter(
                name="type",
                type=OpenApiTypes.STR,
                location="query",
                required=False,
                enum=["internal", "external"],
            ),
            OpenApiParameter(
                name="category_id",
                type=OpenApiTypes.STR,
                location="query",
                required=False,
            ),
            OpenApiParameter(
                name="developer_id",
                type=OpenApiTypes.STR,
                location="query",
                required=False,
            ),
            OpenApiParameter(
                name="q",
                type=OpenApiTypes.STR,
                location="query",
                description="full-text search on name/description",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
