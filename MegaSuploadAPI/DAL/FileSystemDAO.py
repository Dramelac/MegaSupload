import os
from uuid import UUID

from django.conf import settings


# Use File System (for now)
# For testing purpose use null parameter value and hardcoded data

def initRootDirectory(directory):
    os.makedirs(os.path.dirname(settings.ROOT_PATH + directory.getRootPath()))


def store_file(directory, file, file_id, key):
    # TODO encrypt data
    if type(file_id) is UUID:
        file_id = str(file_id)
    path = settings.ROOT_PATH + directory.getRootPath()
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path + file_id, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return "FileKey"


def get_file(directory, fileId, key):
    # TODO check key + decrypt data
    file_data = open(settings.ROOT_PATH + directory.getRootPath() + str(fileId), 'rb')
    data = file_data.read()
    file_data.close()
    return data


def remove_file(directory, fileId):
    try:
        os.remove(settings.ROOT_PATH + directory.getRootPath() + str(fileId))
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
