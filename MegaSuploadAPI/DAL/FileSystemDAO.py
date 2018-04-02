import os

# Use File System (for now)
# For testing purpose use null parameter value and hardcoded data
from uuid import UUID

# TODO move fs_storage to setting file
root_path = "fs_storage"


def initRootDirectory(directory):
    os.makedirs(os.path.dirname(root_path + directory.getRootPath()))


def store_file(directory, file, file_id, key):
    # TODO encrypt data
    if type(file_id) is UUID:
        file_id = str(file_id)
    # TODO move path to setting file
    path = root_path + directory.getRootPath()
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path + file_id, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return "FileKey"


def get_file(directory, fileId, key):
    # TODO check key + decrypt data
    file_data = open(root_path + directory.getRootPath() + str(fileId), 'rb')
    data = file_data.read()
    file_data.close()
    return data


def remove_file(directory, fileId):
    try:
        os.remove(root_path + directory.getRootPath() + str(fileId))
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
