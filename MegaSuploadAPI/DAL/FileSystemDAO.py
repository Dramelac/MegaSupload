import os
from uuid import UUID

from django.conf import settings
from random import randint
from zipfile import ZipFile, ZIP_DEFLATED
from MegaSuploadAPI.DAL import FileDAO, DirectoryDAO


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


def recursive_zip(directory, curr_path, root_dir, zip_file, user):
    file_list = FileDAO.listFiles(directory, user)
    for f in file_list:
        f_name = curr_path + '/' + f['name'] if curr_path is not None else f['name']
        zip_file.write(filename=root_dir + str(f['id']), arcname=f_name)
    dir_list = DirectoryDAO.listDirectory(directory, user)
    for d in dir_list:
        if not 'type' in d:
            dir_obj = DirectoryDAO.getDirectoryFromId(d['id'], user)
            new_curr_path = curr_path + '/' + d['name'] if curr_path is not None else d['name']
            recursive_zip(dir_obj, new_curr_path, root_dir, zip_file, user)


def zip_dir(directory, user):
    zip_file_name = '/tmp/%s.zip' % randint(0, 1000000000)
    root_dir = settings.ROOT_PATH + directory.getRootPath()
    zip_file = ZipFile(zip_file_name, "w", ZIP_DEFLATED)
    recursive_zip(directory, None, root_dir, zip_file, user)
    zip_file.close()
    file_data = open(zip_file_name, 'rb')
    data = file_data.read()
    file_data.close()
    return data

