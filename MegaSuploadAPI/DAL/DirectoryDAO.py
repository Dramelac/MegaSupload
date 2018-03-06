import re

from django.core.exceptions import PermissionDenied, FieldError, ObjectDoesNotExist

from MegaSuploadAPI.DAL import PermissionDAO
from MegaSuploadAPI.models import Directory


# TODO Remove Directory (+ File + Permission linked)
# TODO Share Directory
# TODO Move/Rename Directory

def addDirectory(user, name, parent=None):
    directory = Directory.objects.create(name=name, parent=parent)
    if parent:
        PermissionDAO.inheritPermission(parent, user, directory)
    else:
        PermissionDAO.rootPermission(user, directory)
    return directory


def getDirectoryFromPath(path, user):
    if not re.compile("^/").match(path):
        raise FieldError
    analyze = path.split('/')
    analyze[0] = str(user.id)
    directory = None
    for name in analyze:
        if name == '':
            continue
        directory = Directory.objects.get(name=name, parent=directory)

    perm = PermissionDAO.getPermissionFromDir(directory, user)
    if perm is not None and perm.read:
        return directory
    else:
        raise PermissionDenied


def getDirectoryFromId(dirId, user):
    directory = Directory.objects.get(id=dirId)
    if directory is not None:
        perm = PermissionDAO.getPermissionFromDir(directory, user)
        if perm is not None and perm.read:
            return directory
        else:
            raise PermissionDenied
    else:
        raise ObjectDoesNotExist
