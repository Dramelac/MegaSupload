import os
from uuid import UUID

from django.conf import settings
from random import randint
from zipfile import ZipFile, ZIP_DEFLATED
from MegaSuploadAPI.DAL import FileDAO


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


def zip_dir(directory, user):
    zip_file_name = '/tmp/%s.zip' % randint(0, 1000000000)
    zip_file = ZipFile(zip_file_name, "w", ZIP_DEFLATED)
    file_list = FileDAO.listFiles(directory, user)
    for f in file_list:
        zip_file.write(filename=settings.ROOT_PATH + directory.getRootPath() + str(f['id']), arcname=f['name'])
    zip_file.close()
    file_data = open(zip_file_name, 'rb')
    data = file_data.read()
    file_data.close()
    return data

