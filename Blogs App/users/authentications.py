from .models import User
from jwt import encode, decode
from rest_framework import exceptions, authentication
from datetime import timedelta, datetime
from django.conf import settings


def create_token(id:int, email:str, username:str):
    payload = dict(
        id = id,
        email=email,
        username=username,
        exp=datetime.utcnow() + timedelta(hours=4),
        iat=datetime.utcnow()
    )
    token = encode(payload=payload, key=settings.JWT_SECRET, algorithm="HS256")
    return token


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
