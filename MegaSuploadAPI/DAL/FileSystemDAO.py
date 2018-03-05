# TODO Store File(Data) -> return FileKey
# TODO Get File(FileKey) -> return Data (Or permission Exception -> 404 error code)

import os

# Use File System (for now)
# For testing purpose use null parameter value and hardcoded data

def store_file(path, file):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname('fs_storage'+path))
    with open('fs_storage'+path+file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return "FileKey"


def get_file(filekey):
    file = open('fs_storage'+filekey.file.fullpath(), 'r')
    data = file.read()
    file.close()
    return data
