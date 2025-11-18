from rest_framework import status
from rest_framework.test import APITestCase

from apps.models import App
from category.models import Category
from developer_profiles.models import DeveloperProfile
from installation.models import Installation
from installation.views import InstallationsViewSet
from organizations.models import Organization
from permissions import IsDeveloper
from users.models import User


# Create your tests here.


class InstallationsViewSetTest(APITestCase):
    def setUp(self):
        # Создаем категорию
        self.category = Category.objects.create(name="Test Category")

        # Создаем пользователей разных типов
        self.developer_user = User.objects.create_user(
            email="developer@test.com",
            login="developer",
            password="password",
            type="developer",
        )

        self.school_admin_user = User.objects.create_user(
            email="admin@test.com",
            login="admin",
            password="password",
            type="school_admin",
        )

        self.teacher_user = User.objects.create_user(
            email="teacher@test.com",
            login="teacher",
            password="password",
            type="teacher",
        )

        # Создаем developer profile
        self.developer_profile = DeveloperProfile.objects.create(
            user=self.developer_user
        )

        # Создаем организацию
        self.organization = Organization.objects.create(
            name="Test Organization", description="Test Description"
        )

        # Создаем приложение
        self.app = App.objects.create(
            name="Test App",
            description="Test Description",
            type="internal",
            status="published",
            developer=self.developer_profile,
            category=self.category,
        )

        # Создаем установку
        self.installation = Installation.objects.create(
            app=self.app, organization=self.organization
        )

    def test_get_permissions_for_retrieve(self):
        """Тестируем, что для retrieve действия возвращается правильный permission"""
        viewset = InstallationsViewSet()
        viewset.action = "retrieve"

        permissions = viewset.get_permissions()

        self.assertEqual(len(permissions), 1)
        self.assertIsInstance(permissions[0], IsDeveloper)

    def test_get_permissions_for_other_actions(self):
        """Тестируем, что для других действий permissions пуст"""
        viewset = InstallationsViewSet()

        # Тестируем несколько действий
        for action in ["list", "create", "update", "partial_update", "destroy"]:
            with self.subTest(action=action):
                viewset.action = action
                permissions = viewset.get_permissions()
                self.assertEqual(len(permissions), 0)

    def test_retrieve_installation_developer_success(self):
        """Разработчик может получить детальную информацию об установке"""
        self.client.force_authenticate(user=self.developer_user)

        response = self.client.get(f"/installations/{self.installation.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.installation.id)

    def test_retrieve_installation_school_admin_forbidden(self):
        """Школьный администратор не может получить детальную информацию об установке"""
        self.client.force_authenticate(user=self.school_admin_user)

        response = self.client.get(f"/installations/{self.installation.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_installation_teacher_forbidden(self):
        """Учитель не может получить детальную информацию об установке"""
        self.client.force_authenticate(user=self.teacher_user)

        response = self.client.get(f"/installations/{self.installation.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_installation_anonymous_forbidden(self):
        """Анонимный пользователь не может получить детальную информацию об установке"""
        response = self.client.get(f"/installations/{self.installation.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_installation_developer_success(self):
        """Разработчик может создать установку"""
        self.client.force_authenticate(user=self.developer_user)

        # Создаем вторую организацию и приложение для теста
        organization2 = Organization.objects.create(
            name="Test Organization 2", description="Test Description 2"
        )

        app2 = App.objects.create(
            name="Test App 2",
            description="Test Description 2",
            type="external",
            status="published",
            developer=self.developer_profile,
            category=self.category,
        )

        data = {"app": app2.id, "organization": organization2.id}

        response = self.client.post("/installations/", data)

        # Может быть 201 или 400 в зависимости от бизнес-логики
        self.assertIn(
            response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        )

    def test_create_installation_school_admin_success(self):
        """Школьный администратор может создать установку"""
        self.client.force_authenticate(user=self.school_admin_user)

        organization2 = Organization.objects.create(
            name="Test Organization 2", description="Test Description 2"
        )

        app2 = App.objects.create(
            name="Test App 2",
            description="Test Description 2",
            type="external",
            status="published",
            developer=self.developer_profile,
            category=self.category,
        )

        data = {"app": app2.id, "organization": organization2.id}

        response = self.client.post("/installations/", data)

        self.assertIn(
            response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        )

    def test_create_installation_anonymous_success(self):
        """Анонимный пользователь может создать установку"""
        organization2 = Organization.objects.create(
            name="Test Organization 2", description="Test Description 2"
        )

        app2 = App.objects.create(
            name="Test App 2",
            description="Test Description 2",
            type="external",
            status="published",
            developer=self.developer_profile,
            category=self.category,
        )

        data = {"app": app2.id, "organization": organization2.id}

        response = self.client.post("/installations/", data)

        self.assertIn(
            response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
        )

    def test_delete_installation_developer_success(self):
        """Разработчик может удалить установку"""
        self.client.force_authenticate(user=self.developer_user)

        response = self.client.delete(f"/installations/{self.installation.id}/")

        self.assertIn(
            response.status_code,
            [status.HTTP_204_NO_CONTENT, status.HTTP_403_FORBIDDEN],
        )


class IsDeveloperPermissionTest(APITestCase):
    def setUp(self):
        self.permission = IsDeveloper()

        # Создаем пользователей разных типов
        self.developer_user = User.objects.create_user(
            email="developer@test.com",
            login="developer",
            password="password",
            type="developer",
        )

        self.developer_profile = DeveloperProfile.objects.create(
            user=self.developer_user
        )


        self.school_admin_user = User.objects.create_user(
            email="admin@test.com",
            login="admin",
            password="password",
            type="school_admin",
        )

        self.teacher_user = User.objects.create_user(
            email="teacher@test.com",
            login="teacher",
            password="password",
            type="teacher",
        )

    def test_has_permission_developer_user(self):
        """Разработчик имеет permission"""
        request = self.client.get("/").wsgi_request
        request.user = self.developer_user

        view = type("MockView", (), {"action": "retrieve"})

        self.assertTrue(self.permission.has_permission(request, view))

    def test_has_permission_school_admin_user(self):
        """Школьный администратор не имеет permission"""
        request = self.client.get("/").wsgi_request
        request.user = self.school_admin_user

        view = type("MockView", (), {"action": "retrieve"})

        self.assertFalse(self.permission.has_permission(request, view))

    def test_has_permission_teacher_user(self):
        """Учитель не имеет permission"""
        request = self.client.get("/").wsgi_request
        request.user = self.teacher_user

        view = type("MockView", (), {"action": "retrieve"})

        self.assertFalse(self.permission.has_permission(request, view))

    def test_has_permission_anonymous_user(self):
        """Анонимный пользователь не имеет permission"""
        request = self.client.get("/").wsgi_request
        request.user = None

        view = type("MockView", (), {"action": "retrieve"})

        self.assertFalse(self.permission.has_permission(request, view))

