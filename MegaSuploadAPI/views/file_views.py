import json
from json import JSONDecodeError

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, FieldError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from MegaSuploadAPI.DAL import FileSystemDAO, DirectoryDAO, FileDAO, FileKeyDAO, PermissionDAO
from MegaSuploadAPI.forms import *


@login_required
@require_http_methods(["POST"])
def upload(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        dirId = request.POST.get("dirId")
        try:
            directory = DirectoryDAO.getDirectoryFromId(dirId, request.user)
        except (ObjectDoesNotExist, PermissionDenied):
            return JsonResponse({"message": "Not found"}, status=404)
        except FieldError:
            return JsonResponse({"message": "Bad input"}, status=400)

        file = request.FILES['file']
        FileDAO.uploadFile(file, directory, request.user)

        return JsonResponse({"message": "Success."}, status=200)
    return JsonResponse({"message": "Error invalid input."}, status=400)


@login_required
def download(request):
    dirId = request.GET.get("did")
    fileId = request.GET.get("fid")
    try:
        directory = DirectoryDAO.getDirectoryFromId(dirId, request.user)
        file = FileDAO.getFileFromId(fileId, request.user)
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)
    except FieldError:
        return JsonResponse({"message": "Bad input"}, status=400)

    try:
        file_data = FileSystemDAO.get_file(directory, file.id, "")  # TODO add FileKey
        response = HttpResponse(file_data, content_type=file.type)
        response['Content-Disposition'] = 'inline; filename=' + file.name
        return response
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Not found"}, status=404)


@csrf_exempt
@login_required
def test(request):
    # test API method
    # put your code here ok
    user = request.user
    file = FileDAO.getFileFromId('40080269-6423-4810-b2f4-d51ff7578eec', user=user)
    FileKeyDAO.newFileKey(user, file)
    # fileKey = FileKeyDAO.getFileKey(user, file)

    return JsonResponse({"message": "Executed"}, status=200)


@login_required
def ls(request):
    dirId = request.GET.get("did", '')
    if not dirId:
        directory = DirectoryDAO.getRootDirectory(request.user)
    else:
        try:
            directory = DirectoryDAO.getDirectoryFromId(dirId, request.user)
        except (ObjectDoesNotExist, PermissionDenied):
            return JsonResponse({"message": "Not found"}, status=404)
        except FieldError:
            return JsonResponse({"message": "Bad input"}, status=400)

    dirList = DirectoryDAO.listDirectory(directory, request.user)
    fileList = FileDAO.listFiles(directory, request.user)
    return JsonResponse({"directory": dirList, "file": fileList}, status=200)


@login_required
def addDirectory(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except JSONDecodeError:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    dirId = data.get('dirId', '').strip()
    name = data.get('name', '').strip()
    user = request.user

    try:
        directory = DirectoryDAO.getDirectoryFromId(dirId, user)
        perm = PermissionDAO.getPermission(directory, user)
        if not (perm.edit or perm.owner):
            raise PermissionDenied
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)
    except FieldError:
        return JsonResponse({"message": "Bad input"}, status=400)

    DirectoryDAO.addDirectory(user, name, directory)
    return JsonResponse({"message": "Success"}, status=200)


@login_required
def renameDirectory(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except JSONDecodeError:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    elementId = data.get('uuid', '').strip()
    name = data.get('name', '').strip()
    if not elementId or not name:
        return JsonResponse({"message": "Bad input"}, status=400)
    user = request.user

    try:
        directory = DirectoryDAO.getDirectoryFromId(elementId, request.user)
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)
    except FieldError:
        return JsonResponse({"message": "Bad input"}, status=400)

    DirectoryDAO.rename(directory, name, user)
    return JsonResponse({"message": "Success"}, status=200)


@login_required
def renameFile(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except JSONDecodeError:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    elementId = data.get('uuid', '').strip()
    name = data.get('name', '').strip()
    if not elementId or not name:
        return JsonResponse({"message": "Bad input"}, status=400)
    user = request.user

    try:
        file = FileDAO.getFileFromId(elementId, request.user)
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)
    except FieldError:
        return JsonResponse({"message": "Bad input"}, status=400)

    FileDAO.rename(file, name, user)
    return JsonResponse({"message": "Success"}, status=200)


@login_required
def moveDir(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except JSONDecodeError:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    dirId = data.get('dirId', '').strip()
    targetDirId = data.get('targetDirId', '').strip()
    if not dirId or not targetDirId or dirId == targetDirId:
        return JsonResponse({"message": "Bad input"}, status=400)

    user = request.user

    try:
        directory = DirectoryDAO.getDirectoryFromId(dirId, request.user)
        parentDir = DirectoryDAO.getDirectoryFromId(targetDirId, request.user)
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)
    except FieldError:
        return JsonResponse({"message": "Bad input"}, status=400)

    DirectoryDAO.moveDirectory(directory, parentDir, user)
    return JsonResponse({"message": "Success"}, status=200)


@login_required
def moveFile(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except JSONDecodeError:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    fileId = data.get('fileId', '').strip()
    dirId = data.get('dirId', '').strip()
    user = request.user

    try:
        file = FileDAO.getFileFromId(fileId, request.user)
        directory = DirectoryDAO.getDirectoryFromId(dirId, request.user)
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)
    except FieldError:
        return JsonResponse({"message": "Bad input"}, status=400)

    FileDAO.move(file, directory, user)
    return JsonResponse({"message": "Success"}, status=200)

# TODO GetFileKey
