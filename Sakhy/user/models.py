from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import MinLengthValidator

class UserManager(BaseUserManager):
    def create_user(self, username, email, phone, wallet):
        user = self.model()
        user.username = username
        user.email = email
        user.phone = phone
        user.wallet = wallet

        user.save()
        return user

    def create_superuser(self, username, phone):
        user = self.create_user(
            username=username,
            phone=phone
            )
        
        user.save()
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True, blank=True)
    phone = models.CharField(max_length=9, validators=[MinLengthValidator(limit_value=9)], unique=True)
    wallet = models.IntegerField(blank=True)
    

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

