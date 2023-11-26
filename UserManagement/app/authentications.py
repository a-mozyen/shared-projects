from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from datetime import timedelta, datetime
from django.conf import settings
import jwt


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.COOKIES.get("jwt")
            
            if not token:
                return None
            
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            user = User.objects.get(id=payload["id"])

        except:
            raise AuthenticationFailed("Unauthorized")

        return (user, None)



def create_token(id: int, email: str):
    payload = dict(
        id=id,
        email=email,
        exp=datetime.utcnow() + timedelta(hours=4),
        iat=datetime.utcnow(),
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token
