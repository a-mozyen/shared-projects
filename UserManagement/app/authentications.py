from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .models import User


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

        except:
            raise AuthenticationFailed("Unauthorized")

        user = User.objects.get(id=payload["id"])

        return (user, None)
