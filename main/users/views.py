from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from users.jwt_utils import JWTService
from users.schemes import register_schema, login_schema
from users.serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer


class RegisterView(APIView):
    @register_schema
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        except ValidationError as e:
            return Response({"Error": e.detail}, status=status.HTTP_409_CONFLICT)

        jwt_service = JWTService()
        access_token, refresh_token = jwt_service.create_token(user)

        return Response(
            {
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
                "user": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    @login_schema
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"Error": serializer.errors},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = serializer.validated_data['user']
        jwt_service = JWTService()
        access_token, refresh_token = jwt_service.create_token(user)

        return Response(
            {
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
                "user": UserProfileSerializer(user).data,
            },
            status=status.HTTP_200_OK
        )
