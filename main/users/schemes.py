from drf_spectacular.utils import extend_schema, OpenApiResponse

from users.serializers import RegisterSerializer

register_schema = extend_schema(
    summary="Register a new user",
    description="Creates a new user and issues authorization tokens.",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(description="User has been successfully registered"),
        400: OpenApiResponse(description="Validation error"),
        409: OpenApiResponse(description="User with this email/login already exists"),
    },
    tags=["users"],
)
