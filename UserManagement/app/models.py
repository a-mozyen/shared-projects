from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, last_login, is_active, is_staff, is_superuser) -> "User":
        user = self.model(email = self.normalize_email(email))
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.last_login = last_login
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user
    
    def create_superuser(self, first_name, last_name, email, password) -> "User":
        user = self.create_user(first_name=first_name, last_name=last_name, email=email, password=password, last_login=True, is_active=True, is_staff=True, is_superuser=True)
        user.save()
        return user

class User(AbstractBaseUser):
    id = models.AutoField(verbose_name='user id', primary_key=True)
    first_name = models.CharField(verbose_name='First Name', max_length=255)
    last_name = models.CharField(verbose_name='Last Name', max_length=255)
    email = models.EmailField(verbose_name='Email Adress', max_length=255, unique=True)
    password = models.CharField(verbose_name='Password', max_length=255, null=False, blank=False)
    last_login = models.DateTimeField(verbose_name='Last login', auto_now = True)
    is_active = True
    is_staff = False
    is_superuser = False

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)