from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from MegaSuploadAPI.DAL import PermissionDAO
from MegaSuploadAPI.models import Directory


# TODO Remove Directory (+ File + Permission linked)

def addDirectory(user, name, parent=None):
    directory = Directory.objects.create(name=name, parent=parent)
    if parent:
        PermissionDAO.inheritPermission(parent, user, directory)
    else:
        PermissionDAO.rootPermission(user, directory)
    return directory


def getRootDirectory(user):
    return Directory.objects.get(name=user.id, parent=None)


""" # Old deprecated method
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

    perm = PermissionDAO.getPermission(directory, user)
    # Only owner can use this interface // for now
    if perm is not None and perm.owner:
        return directory
    else:
        raise PermissionDenied
"""


def getDirectoryFromId(dirId, user):
    directory = Directory.objects.get(id=dirId)
    if directory is not None:
        perm = PermissionDAO.getPermission(directory, user)
        if perm is not None and (perm.owner or perm.read):
            return directory
        else:
            raise PermissionDenied
    else:
        raise ObjectDoesNotExist


def listDirectory(directory, user):
    dirList = Directory.objects.filter(parent=directory)
    result = []
    dirPerm = PermissionDAO.getPermission(directory, user)
    for tempDir in dirList:
        perm = PermissionDAO.getPermission(tempDir, user)
        if dirPerm.read or (perm is not None and perm.read):
            result.append((tempDir.name, tempDir.id))
    result.append(('.', directory.id))
    parent = directory.parent
    if parent is not None:
        result.append(('..', parent.id))
    return result


def rename(directory, newname, user):
    perm = PermissionDAO.getPermission(directory, user)
    if perm.edit:
        directory.name = newname
        directory.save()
    else:
        raise PermissionDenied


def moveDirectory(directory, newParent, user):
    perm = PermissionDAO.getPermission(directory, user)
    if perm.edit:
        directory.parent = newParent
        directory.save()
    else:
        raise PermissionDenied


# Only for owner (for now)
def removeDirectory(directory, user):
    perm = PermissionDAO.getPermission(directory, user)
    if perm.owner:
        # TODO Add file removed
        # dirList = Directory.objects.filter(parent=directory)
        directory.delete()  # Cascade delete ?
        # FK problem ? to test
