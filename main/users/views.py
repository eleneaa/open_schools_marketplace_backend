from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from users.jwt_utils import JWTService
from users.schemes import register_schema
from users.serializers import RegisterSerializer


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
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
