from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from users.serializers import RegisterSerializer, RegisterConflictErrorSerializer
from users.serializers import LoginSerializer, UserProfileSerializer

register_schema = extend_schema(
    summary="Register a new user",
    description="Creates a new user and issues authorization tokens.",
    request=RegisterSerializer,
    responses={
        201: RegisterSerializer,
        400: OpenApiResponse(description="Validation error"),
        409: OpenApiResponse(
            description="User with this email/login already exists",
            response=RegisterConflictErrorSerializer,
            examples=[
                OpenApiExample(
                    "Missing field",
                    value={"Error": {"login": ["This field is required."]}},
                    status_codes=["409"],
                ),
                OpenApiExample(
                    "Email/login already exist",
                    value={
                        "Error": {
                            "email": ["user with this email already exists."],
                            "login": ["user with this login already exists."],
                        }
                    },
                    status_codes=["409"],
                ),
            ],
        ),
    },
    tags=["users"],
)

login_schema = extend_schema(
    summary="User login",
    description="Authenticate user and return JWT tokens and user profile",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            response=UserProfileSerializer,
            description="Successful authentication",
            examples=[
                OpenApiExample(
                    "Success Response",
                    value={
                        "token": {
                            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                        },
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "login": "username",
                            "type": "developer"
                        }
                    }
                )
            ]
        ),
        401: OpenApiResponse(
            description="Invalid credentials",
            examples=[
                OpenApiExample(
                    "Invalid credentials",
                    value={"error": {"non_field_errors": ["invalid_credentials"]}}
                )
            ]
        )
    },
    tags=["users"],
)