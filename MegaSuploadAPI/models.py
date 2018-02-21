from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=True)
    edit = models.BooleanField(default=True)
    share = models.BooleanField(default=True)
    owner = models.BooleanField(default=True)
