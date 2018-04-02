from MegaSuploadAPI.models import Permission, File


def rootPermission(user, directory):
    Permission.objects.create(user=user, directory=directory, read=True, edit=True, share=True, owner=True)


# When creating new item, inherit permission from parent directory
def inheritPermission(parent, user, element):
    model = Permission.objects.get(directory=parent, user=user)
    if model is None:
        raise Exception('Parent directory not found')

    isFile = type(element) is File
    if model.user == user and model.edit:
        if not model.owner:
            ownerPerm = Permission.objects.get(directory=parent, owner=True)
            build = Permission(user=ownerPerm.user, read=ownerPerm.read, edit=ownerPerm.edit,
                               share=ownerPerm.share, owner=True)
            if isFile:
                build.file = element
            else:
                build.directory = element
            build.save()
        build = Permission(user=user, read=model.read, edit=model.edit, share=model.share, owner=model.owner)
        if isFile:
            build.file = element
        else:
            build.directory = element
        build.save()


# Allow to share directory or file
def share(user, userTarget, element, read, write, share):
    isFile = type(element) is File
    if write and not read:
        raise Exception('Inconsistent permission')
    perm = Permission.objects.get(file=element, user=user) if isFile else \
        Permission.objects.get(directory=element, user=user)
    if perm is not None and (perm.share or perm.owner):
        build = Permission(user=userTarget, read=read, edit=write, share=share)
        if isFile:
            build.file = element
        else:
            build.directory = element
        build.save()
    else:
        raise Exception('Insufficient permission')


# Update permission of a specific user // Only for file/directory owner
def update(user, userTarget, element, read, write, share):
    isFile = type(element) is File
    if write and not read:
        raise Exception('Inconsistent permission')
    perm = Permission.objects.get(file=element, user=user) if isFile else \
        Permission.objects.get(directory=element, user=user)
    if perm is not None and perm.owner:
        targetPerm = Permission.objects.get(file=element, user=userTarget) if isFile else \
            Permission.objects.get(directory=element, user=userTarget)
        if targetPerm is not None:
            targetPerm.read = read
            targetPerm.edit = write
            targetPerm.share = share
            targetPerm.save()
    else:
        raise Exception('Insufficient permission')


# Remove permission of a specific user // Only for file/directory owner
def remove(user, userTarget, element):
    isFile = type(element) is File
    perm = Permission.objects.get(file=element, user=user) if isFile else \
        Permission.objects.get(directory=element, user=user)
    if perm is not None and perm.owner:
        targetPerm = Permission.objects.get(file=element, user=userTarget) if isFile else \
            Permission.objects.get(directory=element, user=userTarget)
        if targetPerm is not None:
            targetPerm.delete()
    else:
        raise Exception('Insufficient permission')


def getPermission(element, user):
    if type(element) == File:
        return Permission.objects.get(user=user, file=element)
    return Permission.objects.get(user=user, directory=element)


def getOwner(element):
    if type(element) == File:
        return Permission.objects.get(owner=True, file=element)
    return Permission.objects.get(owner=True, directory=element)
