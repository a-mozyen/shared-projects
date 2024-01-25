from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, last_login, is_active, is_admin):
        user = self.model()
        user.username = username
        user.email = email
        user.password = password
        user.last_login = last_login
        user.is_active = is_active
        user.is_admin = is_admin

        user.save()
        return user

    def create_superuser(self, username, password, last_login, email):
        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                last_login=last_login,
                                is_admin=True,
                                is_active=True
                                )
        user.save()
        return user


class User(AbstractBaseUser):
    id = models.AutoField(verbose_name='Id', primary_key=True, auto_created=True)
    username = models.CharField(verbose_name='Username', max_length=255, unique=True)
    email = models.EmailField(verbose_name='Email adress', max_length=255, unique=True)
    password = models.CharField(verbose_name='Password', max_length=255)
    last_login = models.DateTimeField(verbose_name='Last login', null=True, blank=True)
    is_active = True
    is_admin = False

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])