from datetime import datetime, timezone, timedelta
from typing import Optional

import jwt

import settings
from users.models import User


class JWTService:
    def create_token(self, user: User) -> tuple[str, str]:
        time_now = datetime.now(timezone.utc)

        access_payload = {
            "user_id": user.id,
            "email": user.email,
            "type": "access",
            "iat": time_now,
            "exp": time_now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME),
        }

        refresh_payload = {
            "user_id": user.id,
            "email": user.email,
            "type": "refresh",
            "iat": time_now,
            "exp": time_now + timedelta(days=settings.JWT_REFRESH_TOKEN_LIFETIME),
        }

        access_token = jwt.encode(
            access_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        refresh_token = jwt.encode(
            refresh_payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

        return access_token, refresh_token

    def decode_token(self, token: str) -> Optional[dict]:
        decode = jwt.decode(
            jwt=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return decode
