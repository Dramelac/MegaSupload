from random import randint
from uuid import UUID
from zipfile import ZipFile, ZIP_DEFLATED

from django.conf import settings

from MegaSuploadAPI.DAL import FileDAO, DirectoryDAO
from MegaSuploadAPI.tools.cryptool import *


# Use File System (for now)
# For testing purpose use null parameter value and hardcoded data

def initRootDirectory(directory):
    os.makedirs(os.path.dirname(settings.ROOT_PATH + directory.getRootPath()))


def store_file(directory, file, file_id, key):
    if type(file_id) is UUID:
        file_id = str(file_id)
    path = settings.ROOT_PATH + directory.getRootPath()
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path + file_id, 'wb+') as destination:
        iv = ''.join(chr(random.randint(0, 0xFF)) for _ in range(16))
        encryptor = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        destination.write(struct.pack('<Q', file.size))
        destination.write(iv.encode("utf-8"))
        for chunk in file.chunks(CHUNK_SIZE):
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                tmp = ' ' * (16 - len(chunk) % 16)
                chunk += tmp.encode('utf-8')

            destination.write(encryptor.encrypt(chunk))


def get_file(directory, fileId, key):

    with open(settings.ROOT_PATH + directory.getRootPath() + str(fileId), 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        data = b''

        while True:
            chunk = infile.read(16)
            if len(chunk) == 0:
                break
            data += decryptor.decrypt(chunk)

        data.truncate(origsize)


def __get_file(directory, fileId, key):
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
