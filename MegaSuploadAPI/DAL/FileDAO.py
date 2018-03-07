# TODO Remove File (+ FileKey / Permission linked)
# TODO Update File (TODO LATER)
# TODO Move/Rename File

# /!\ This DAO DON'T interact with FileSystem !!! (only file indexing) Use FileSystemDAO for file storage !

from MegaSuploadAPI.DAL import PermissionDAO, FileSystemDAO
from MegaSuploadAPI.models import File


def _newFile(file, directory, user):
    build_file = File.objects.create(directory=directory, name=file.name, type=file.content_type)
    PermissionDAO.inheritPermission(directory, user, build_file)

    # TODO Add FileKey
    FileSystemDAO.store_file(directory, file, build_file.id)


# This method permit to avoid name duplicate on a sam directory
def uploadFile(file, directory, user):
    result = File.objects.filter(directory=directory, name=file.name)
    if len(result) > 0:
        # existing file
        pass
    else:
        # new file
        _newFile(file, directory, user)
