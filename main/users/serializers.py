from django.core.validators import validate_email
from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "login", "password"]

    def validate_email(self, value):
        validate_email(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("The user with this email already exists")
        return value

    def validate_login(self, value):
        if User.objects.filter(login=value).exists():
            raise serializers.ValidationError("The user with this login already exists")
        return value

    def create(self, validated_data):
        validated_data["type"] = "developer"
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)

        return user


class RegisterConflictErrorSerializer(serializers.Serializer):
    Error = serializers.DictField(
        child=serializers.ListField(child=serializers.CharField())
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'login', 'type']  # required profile fields