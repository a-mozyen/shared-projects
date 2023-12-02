from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from datetime import timedelta, datetime
import jwt


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.COOKIES.get("jwt")

            if not token:
                return None

            payload = jwt.decode(token, "jwt-secret", algorithms=["HS256"])
            user = User.objects.get(id=payload["id"])

        except:
            raise AuthenticationFailed("Unauthorized")

        return (user, None)


def create_token(id: int, username: str, email: str):
    payload = dict(
        id=id,
        username=username,
        email=email,
        exp=datetime.utcnow() + timedelta(hours=2),
        iat=datetime.utcnow(),
    )
    token = jwt.encode(payload, "jwt-secret", algorithm="HS256")
    return token
