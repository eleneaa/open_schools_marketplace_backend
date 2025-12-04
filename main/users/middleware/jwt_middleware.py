import time

import jwt
from django.http import HttpRequest, JsonResponse
from django.utils.deprecation import MiddlewareMixin

from users.jwt_utils import JWTService
from users.models import User
from users.user_service import UserService


class JWTMiddleware(MiddlewareMixin):
    def __call__(self, request: HttpRequest, *args, **kwargs):
        request_authorization = request.headers.get("Authorization")

        if not request_authorization or not request_authorization.startswith("Bearer"):
            return JsonResponse({"Error": "Unauthorized"}, status=401)

        try:
            token = request_authorization.split()[1]

            jwt_service = JWTService()
            user_service = UserService()

            payload = jwt_service.decode_token(token=token)
            time_now = time.time()

            if payload["exp"] < int(time_now):
                raise jwt.decode.InvalidTokenError

            user_id = payload["user_id"]
            user = user_service.get_user_by_user_id(id=user_id)

        except (
            jwt.InvalidTokenError,
            jwt.DecodeError,
            User.DoesNotExist,
        ):
            return JsonResponse({"Error": "Unauthorized"}, status=401)

        else:
            request.user = user
            request.user_id = user_id
            request.user_role = user.type

        return self.get_response(request)
