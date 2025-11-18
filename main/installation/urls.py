from django.urls import path

from installation.views import InstallationsViewSet

urlpatterns = [
    path(
        "<int:pk>/",
        InstallationsViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "",
        InstallationsViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
]
