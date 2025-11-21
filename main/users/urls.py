from django.urls import path

from users.views import RegisterView

urlpatterns = [
    path("auth/register/", RegisterView.as_view())
]
