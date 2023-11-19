from datetime import timedelta, datetime
from django.conf import settings
from .models import User
import jwt


def create_token(id: int, email: str):
    payload = dict(
        id=id,
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
