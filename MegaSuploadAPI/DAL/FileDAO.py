# TODO Remove File (+ FileKey / Permission linked)

# /!\ This DAO DON'T interact with FileSystem !!! (only file indexing) Use FileSystemDAO for file storage !
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from MegaSuploadAPI.DAL import PermissionDAO, FileSystemDAO
from MegaSuploadAPI.models import File


def _newFile(file, directory, user):
    build_file = File.objects.create(directory=directory, name=file.name, type=file.content_type)
    PermissionDAO.inheritPermission(directory, user, build_file)

    # TODO Add FileKey
    FileSystemDAO.store_file(directory, file, build_file.id)


def _updateFile(file, file_fs, directory, user):
    perm = PermissionDAO.getPermission(file_fs, user)
    dirPerm = PermissionDAO.getPermission(directory, user)

    if (perm is not None and (perm.owner or perm.edit)) or \
            (dirPerm is not None and (dirPerm.owner or dirPerm.edit)):
        # TODO Add FileKey
        FileSystemDAO.store_file(directory, file, file_fs.id)
    else:
        raise PermissionError


# This method permit to avoid name duplicate on a same directory
def uploadFile(file, directory, user):
    try:
        result = File.objects.get(directory=directory, name=file.name)
        # existing file -> update
        _updateFile(file, result, directory, user)
    except ObjectDoesNotExist:
        # new file
        _newFile(file, directory, user)


def rename(file, newname, user):
    perm = PermissionDAO.getPermission(file, user)
    if perm.owner or perm.edit:
        file.name = newname
        file.save()
    else:
        raise PermissionDenied


def move(file, newDirectory, user):
    perm = PermissionDAO.getPermission(file, user)
    if perm.edit:
        file.directory = newDirectory
        file.save()
    else:
        raise PermissionDenied


def getFileFromId(fileId, user):
    file = File.objects.get(id=fileId)
    if file is not None:
        perm = PermissionDAO.getPermission(file, user)
        if perm is not None and (perm.owner or perm.read):
            return file
        else:
            raise PermissionDenied
    else:
        raise ObjectDoesNotExist


def listFiles(directory, user):
    dirPerm = PermissionDAO.getPermission(directory, user)
    fileList = File.objects.filter(directory=directory)
    result = []
    for file in fileList:
        if dirPerm is not None and dirPerm.read:
            result.append((file.name, file.id))
        else:
            perm = PermissionDAO.getPermission(file, user)
            if perm is not None and perm.read:
                result.append((file.name, file.id))
    return result
