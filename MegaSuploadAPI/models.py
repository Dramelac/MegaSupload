from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=True)
    edit = models.BooleanField(default=True)
    share = models.BooleanField(default=True)
    owner = models.BooleanField(default=True)

class Directory (models.Model):
    path = models.CharField(max_length=4096)
    name =models.CharField(max_length=255)
    parent  = models.ForeignKey('self',on_delete= models.CASCADE())
    permission = models.ForeignKey(Permission,on_delete= models.CASCADE())






