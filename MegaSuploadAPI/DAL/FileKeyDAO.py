from django.core.exceptions import ObjectDoesNotExist

from MegaSuploadAPI.models import FileKey
import random
import string


def newFileKey(owner, file):
    key = ''.join(random.choice(string.ascii_letters + string.digits))
    FileKey.objects.create(owner=owner, file=file, key=key)


def remove(owner, file):
    key = FileKey.objects.get(file=file, owner=owner)
    if key is not None:
        key.delete()


def getFileKey(owner, file):
    fileKey = FileKey.objects.get(file=file, owner=owner)
    if fileKey is not None:
        return fileKey
    else:
        raise ObjectDoesNotExist
