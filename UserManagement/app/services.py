from datetime import timedelta, datetime
from django.conf import settings
from .models import User
import jwt


def create_token(id: int, first_name: str, last_name: str, email: str) -> str:
    payload = dict(
        id=id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        exp=datetime.utcnow() + timedelta(minutes=30),
        iat=datetime.utcnow(),
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token


def user_identefier(email: str):
    user = User.objects.filter(email=email).first()
    return user
