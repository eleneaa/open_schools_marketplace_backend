from django.urls import path

from users.views import RegisterView, LoginView

urlpatterns = [path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
]