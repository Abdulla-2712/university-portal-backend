# your_app/auth.py

import jwt
from django.conf import settings
from ninja.security import HttpBearer
from ninja.errors import HttpError

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload  # You can return user object here if needed
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Token has expired")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Invalid token")
