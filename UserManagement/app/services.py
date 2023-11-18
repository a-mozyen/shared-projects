from datetime import timedelta, datetime
from django.conf import settings
from .models import User
from .serializers import UserSerializer
from rest_framework import exceptions
import jwt


def create_token(id: int, first_name: str, last_name: str, email: str) -> str:
    payload = dict(
        id=id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        exp=datetime.utcnow() + timedelta(hours=8),
        iat=datetime.utcnow(),
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token


def user_identefier(email: str):
    # .first() will limit the filter to one, the first record with that data
    user = User.objects.filter(email=email).first() 
    return user


def get_user(request):
    token = request.COOKIES.get("jwt")
    if not token:
        raise exceptions.AuthenticationFailed('Permission denied, Login to access this page.')
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Token has expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid token. Please log in again.')
    
    user = User.objects.get(id=payload['id'])
    serializer = UserSerializer(user)

    return serializer.data

