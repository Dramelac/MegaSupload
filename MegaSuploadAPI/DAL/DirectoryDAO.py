from MegaSuploadAPI.DAL import PermissionDAO
from MegaSuploadAPI.models import Directory


# TODO Add Directory
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


def getDirectoryFromPath(path):
    analyze = path.split('/')
