from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, phone, wallet):
        user = self.model()
        user.username = username
        user.email = email
        user.password = password
        user.phone = phone
        user.wallet = wallet

        user.save()
        return user

    def create_superuser(self, username, email, password, phone):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone
            )
        
        user.save()
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True, blank=True)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, validators=[MinLengthValidator(limit_value=10)], unique=True)
    wallet = models.IntegerField(blank=True)
    income = models.IntegerField()
    
    INCOME_SOURCE_CHOICES = [
        ('job', 'Job'),
        ('freelancer', 'Freelancer'),
        ('other', 'Other')
    ]
    income_source = models.CharField(max_length=15, choices=INCOME_SOURCE_CHOICES, default='job')

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('widower', 'Widower'),
        ('divorced', 'Divorced')
    ]
    marital_status = models.CharField(max_length=15, choices=MARITAL_STATUS_CHOICES, default='single')
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    objects = UserManager()

