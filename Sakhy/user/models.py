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
    

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

