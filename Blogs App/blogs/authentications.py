from users.models import User
from jwt import decode
from rest_framework import exceptions, authentication
from django.conf import settings


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.COOKIES.get("jwt")
            payload = decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            user = User.objects.get(id=payload["id"])
            if not token:
                return None
            
        except:
            raise exceptions.AuthenticationFailed("Unauthorized")
        
        return (user, None)