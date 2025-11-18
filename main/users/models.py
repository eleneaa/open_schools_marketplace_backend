from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, login, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        if not login:
            raise ValueError('Login обязателен')

        user = self.model(
            email=self.normalize_email(email),
            login=login,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, login, password, **extra_fields)

class User(AbstractBaseUser):
    USER_TYPES = (
        ('school_admin', 'School Admin'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('developer', 'Developer'),
        ('marketplace_admin', 'Marketplace Admin'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('disable', 'Disable'),
    )

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=USER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    icon = models.ImageField(upload_to='user_icons/', null=True, blank=True)
    active = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)  # hash

    organizations = models.ManyToManyField('organizations.Organization', related_name='users', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']

    objects = UserManager()

    def __str__(self):
        return f"{self.login} ({self.type})"
