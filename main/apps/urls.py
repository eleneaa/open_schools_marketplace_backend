from django.urls import path

from apps.views import AppViewSet

urlpatterns = [
    path("", AppViewSet.as_view({"get": "list", "post": "create"})),
    path("<int:pk>/", AppViewSet.as_view({"get": "retrieve", "delete": "destroy"})),
]
