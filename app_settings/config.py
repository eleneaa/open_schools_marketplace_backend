import os

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-)@#djte1uunyz)-cjrf1tte^ljapdb=t*ejeo)nhs(4ldifxuz")
DEBUG = os.environ.get("DEBUG", True)

POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", "5432"))

TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")

JWT_ACCESS_TOKEN_LIFETIME = os.environ.get("JWT_ACCESS_TOKEN_LIFETIME", 30)
JWT_REFRESH_TOKEN_LIFETIME = os.environ.get("JWT_REFRESH_TOKEN_LIFETIME", 10)
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "secretkey")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
