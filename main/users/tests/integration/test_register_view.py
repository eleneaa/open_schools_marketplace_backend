import pytest
from django.urls import reverse
from rest_framework import status

from users.models import User


@pytest.mark.django_db
def test_register_success(api_client):
    path = reverse("register")
    payload = {
        "email": "test@mail.com",
        "login": "test_login",
        "password": "asd123",
        "active": "disable",
    }

    response = api_client.post(path=path, data=payload, format="json")
    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED

    assert "token" in data
    assert "access" in data["token"]
    assert "refresh" in data["token"]

    assert "user" in data
    assert data["user"]["email"] == payload["email"]
    assert data["user"]["login"] == payload["login"]

    user = User.objects.get(email=payload["email"])
    assert user.login == payload["login"]
    assert user.type == "developer"


@pytest.mark.django_db
def test_register_email_exists(api_client, get_users):
    user = get_users[0]

    path = reverse("register")
    payload = {
        "email": user.email,
        "login": "login",
        "password": "asd123",
    }

    response = api_client.post(path=path, data=payload, format="json")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Error" in response.data
    assert "email" in response.data["Error"]
    assert "user with this email already exists." in response.data["Error"]["email"]


@pytest.mark.django_db
def test_register_login_exists(api_client, get_users):
    user = get_users[0]

    path = reverse("register")
    payload = {
        "email": "test@email.com",
        "login": user.login,
        "password": "asd123",
    }

    response = api_client.post(path=path, data=payload, format="json")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Error" in response.data
    assert "login" in response.data["Error"]
    assert "user with this login already exists." in response.data["Error"]["login"]


@pytest.mark.django_db
def test_register_invalid_email(api_client):
    path = reverse("register")
    payload = {
        "email": "invalid-email",
        "login": "user123",
        "password": "pass12345",
    }

    response = api_client.post(path=path, data=payload, format="json")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Error" in response.data
    assert "email" in response.data["Error"]
    assert "Enter a valid email address." in response.data["Error"]["email"]


@pytest.mark.django_db
@pytest.mark.parametrize("missing_field", ["email", "login", "password"])
def test_register_missing_required_fields(api_client, missing_field):
    path = reverse("register")
    payload = {
        "email": "a@mail.com",
        "login": "user1",
        "password": "pass12345",
    }

    payload.pop(missing_field)

    response = api_client.post(path=path, data=payload, format="json")

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Error" in response.data
    assert missing_field in response.data["Error"]
    assert "This field is required." in response.data["Error"][missing_field]


@pytest.mark.django_db
def test_register_password_not_returned(api_client):
    path = reverse("register")
    payload = {
        "email": "secret@mail.com",
        "login": "login123",
        "password": "password123",
    }

    response = api_client.post(path=path, data=payload, format="json")

    assert response.status_code == 201
    assert "password" not in response.data["user"]


@pytest.mark.django_db
def test_register_tokens_structure(api_client):
    path = reverse("register")
    payload = {
        "email": "token@mail.com",
        "login": "tokenuser",
        "password": "pass123456",
    }

    response = api_client.post(path=path, data=payload, format="json")
    tokens = response.data["token"]

    assert isinstance(tokens["access"], str)
    assert isinstance(tokens["refresh"], str)
    assert tokens["access"].count(".") == 2
    assert tokens["refresh"].count(".") == 2
