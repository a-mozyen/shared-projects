from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(
        self,
        first_name,
        last_name,
        email,
        password,
        reg_date,
        last_update,
        last_login,
        is_active,
        is_staff,
        is_superuser) -> "User":

        user = self.model()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.password = password
        user.reg_date = reg_date
        user.last_update = last_update
        user.last_login = last_login
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user


    def create_superuser(self, first_name, last_name, email, password, last_login) -> "User":
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            last_login=last_login,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        user.save()
        return user


class User(AbstractBaseUser):
    id = models.AutoField(verbose_name="User id", primary_key=True)
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    email = models.EmailField(verbose_name="Email Adress", max_length=255, unique=True)
    password = models.CharField(verbose_name="Password", max_length=255)
    reg_date = models.DateTimeField(verbose_name="Member since", auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="Last updated", auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = True
    is_staff = False
    is_superuser = False

    objects = UserManager()
    # specifies the field used for identifying a user when logging in
    USERNAME_FIELD = "email"
    # used to specify the fields that are required when creating a superuser
    REQUIRED_FIELDS = []

    # override the save method of the User model to contain the following
    def save(self, *args, **kwargs):
        # reformate the email field to lower case when saved to database
        self.email = self.email.lower()
        # hashing the password field before saving it to database
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    # update last_login field whenever the user login
    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])