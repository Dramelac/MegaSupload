# TODO Store File(Data) -> return FileKey
# TODO Get File(FileKey) -> return Data (Or permission Exception -> 404 error code)

# Use File System (for now)
# For testing purpose use null parameter value and hardcoded data
from os import system


def store_file(path, file):

    return "FileKey"


def get_file(filekey):
    file = open('static/js/main.js','r')
    data = file.read()
    file.close()
    return data