# TODO Store File(Data) -> return FileKey
# TODO Get File(FileKey) -> return Data (Or permission Exception -> 404 error code)

import os


# Use File System (for now)
# For testing purpose use null parameter value and hardcoded data
from uuid import UUID


def initRootDirectory(directory):
    os.makedirs(os.path.dirname('fs_storage' + directory.getRootPath()))


def store_file(directory, file, file_id):
    if type(file_id) is UUID:
        file_id = str(file_id)
    path = 'fs_storage' + directory.getRootPath()
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path + file_id, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return "FileKey"


def get_file(directory, fileId, key):
    file_data = open('fs_storage' + directory.getRootPath() + fileId, 'r')
    data = file_data.read()
    file_data.close()
    return data
