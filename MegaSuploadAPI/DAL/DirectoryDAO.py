from MegaSuploadAPI.models import Directory


# TODO Add Directory
# TODO Remove Directory (+ File + Permission linked)
# TODO Share Directory
# TODO Move/Rename Directory

def addDirectory(name, parent):
    Directory.objects.create(name=name, parent=parent)


def getDirectoryFromPath(path):
    analyze = path.split('/')
