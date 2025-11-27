import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture(scope="function")
def api_client():
    client = APIClient()
    return client


@pytest.fixture(scope="function")
def get_users():
    users = []
    types = ("school_admin", "developer", "marketplace_admin")

    for i in range(3):
        users.append(
            User.objects.create(
                type=types[i],
                email=f"user_{i}@mail.com",
                login=f"user_login_{i}",
                password="password",
            )
        )

    return users
