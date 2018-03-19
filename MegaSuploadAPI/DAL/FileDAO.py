# TODO Remove File (+ FileKey / Permission linked)

# /!\ This DAO DON'T interact with FileSystem !!! (only file indexing) Use FileSystemDAO for file storage !
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied

from MegaSuploadAPI.DAL import PermissionDAO, FileSystemDAO, FileKeyDAO
from MegaSuploadAPI.models import File


def _newFile(file, directory, user):
    if user.data_used + file.size > user.max_data_allowed:
        raise PermissionError
    build_file = File.objects.create(directory=directory, name=file.name, type=file.content_type, size=file.size)
    PermissionDAO.inheritPermission(directory, user, build_file)

    key = FileKeyDAO.newFileKey(owner=user, file=build_file)
    FileSystemDAO.store_file(directory, file, build_file.id, key)

    # TODO check data relative to owner
    user.data_used += file.size
    user.save()


def _updateFile(file, file_fs, directory, user, key):
    oldSize = file_fs.size
    if user.data_used - oldSize + file.size > user.max_data_allowed:
        raise PermissionError
    perm = PermissionDAO.getPermission(file_fs, user)
    dirPerm = PermissionDAO.getPermission(directory, user)

    if (perm is not None and (perm.owner or perm.edit)) or \
            (dirPerm is not None and (dirPerm.owner or dirPerm.edit)):
        FileSystemDAO.store_file(directory, file, file_fs.id, key)
    else:
        raise PermissionDenied

    # TODO check data relative to owner
    user.data_used -= oldSize
    user.data_used += file.size
    user.save()

    file_fs.size = file.size
    file_fs.save()


# This method permit to avoid name duplicate on a same directory
def uploadFile(file, directory, user, key=None):
    try:
        result = File.objects.get(directory=directory, name=file.name)
        perm = PermissionDAO.getPermission(result, user)
        # existing file -> update
        if key is not None and perm is not None and perm.edit:
            _updateFile(file, result, directory, user, key)
        else:
            raise PermissionDenied
    except ObjectDoesNotExist:
        # new file
        _newFile(file, directory, user)


def isFileExist(fileName, directoryId, user):
    try:
        result = File.objects.get(directory=directoryId, name=fileName)
        perm = PermissionDAO.getPermission(result, user)
        return perm is not None and perm.read
    except ObjectDoesNotExist:
        return False


def rename(file, newname, user):
    if not isFileExist(newname, file.directory, user):
        raise FileExistsError
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
    fileList = File.objects.filter(directory=directory).values()
    result = []
    for file in fileList:
        if dirPerm is not None and dirPerm.read:
            result.append(file)
        else:
            perm = PermissionDAO.getPermission(file, user)
            if perm is not None and perm.read:
                result.append(file)
    return list(result)


def remove(fileId, user):
    file = getFileFromId(fileId, user)
    perm = PermissionDAO.getPermission(file, user)
    if perm is not None and perm.owner:
        PermissionDAO.remove(user, user, file)
        dataSize = file.size
        file.delete()
        user.data_used -= dataSize
        if user.data_used < 0:
            user.data_used = 0
        user.save()


def getFileIdFromName(fileName, directoryId, user):
    try:
        file = File.objects.get(directory=directoryId, name=fileName)
        perm = PermissionDAO.getPermission(file, user)
        if perm is not None and perm.read:
            return file.id

    except ObjectDoesNotExist:
        return None
