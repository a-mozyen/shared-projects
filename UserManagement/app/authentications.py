from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .models import User


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.COOKIES.get("jwt")
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            user = User.objects.get(id=payload["id"])

        except:
            raise AuthenticationFailed("Unauthorized")

        return (user,)
