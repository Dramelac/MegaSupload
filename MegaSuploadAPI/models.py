from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    space_allowed = models.IntegerField(default=30)
    pub_key = models.TextField()
    encrypted_priv_key = models.TextField()


class Directory (models.Model):
    path = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.path, self.name)


class File(models.Model):
    path = models.CharField(max_length=4096)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return "%s - %s" % (self.path, self.name)

    def fullpath(self):
        return self.path+"/"+self.name


class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=True)
    edit = models.BooleanField(default=False)
    share = models.BooleanField(default=False)
    owner = models.BooleanField(default=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "%s - Read: %d, Edit: %d, Share: %d, Owner: %d" % (self.user.username, self.read, self.edit, self.share, self.owner)


class FileKey(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    key = models.TextField()

    def __str__(self):
        return "%s - %s" % (self.owner.username, self.file.name)
