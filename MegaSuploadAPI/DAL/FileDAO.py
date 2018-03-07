# TODO Remove File (+ FileKey / Permission linked)
# TODO Update File (TODO LATER)
# TODO Move/Rename File

# /!\ This DAO DON'T interact with FileSystem !!! (only file indexing) Use FileSystemDAO for file storage !
from django.core.exceptions import ObjectDoesNotExist

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
