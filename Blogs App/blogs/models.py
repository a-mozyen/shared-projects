from django.db import models
from users.models import User

class Blogs(models.Model):
    id = models.AutoField(verbose_name='Id', primary_key=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    blog_title = models.CharField(verbose_name='Title', max_length=255, unique=True)
    body = models.TextField(verbose_name='Body')
    created = models.DateTimeField(verbose_name='Publish date', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Update date', auto_now=True)
