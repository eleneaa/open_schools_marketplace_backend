from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from users.serializers import RegisterSerializer, RegisterConflictErrorSerializer

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
