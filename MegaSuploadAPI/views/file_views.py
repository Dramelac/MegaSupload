import json
import urllib
from json import JSONDecodeError

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, FieldError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from MegaSuploadAPI.DAL import FileSystemDAO, DirectoryDAO, FileDAO, PermissionDAO, FileKeyDAO, UserDAO
from MegaSuploadAPI.forms import *
from MegaSuploadAPI.models import File
from MegaSuploadAPI.tools.tools import is_uuid


@login_required
@require_http_methods(["POST"])
def upload(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        dirId = request.POST.get("dirId")
        key = request.POST.get("key")
        try:
            directory = DirectoryDAO.getDirectoryFromId(dirId, request.user)
        except (ObjectDoesNotExist, PermissionDenied):
            return JsonResponse({"message": "Not found"}, status=404)
        except FieldError:
            return JsonResponse({"message": "Bad input"}, status=400)

        file = request.FILES['file']
        try:
            FileDAO.uploadFile(file, directory, request.user, key)
        except PermissionDenied:
            return JsonResponse({"message": "Not found"}, status=404)
        except PermissionError:
            return JsonResponse({"message": "Not enough data space"}, status=400)

        return JsonResponse({"message": "Success."}, status=200)
    return JsonResponse({"message": "Error invalid input."}, status=400)


@login_required
@require_http_methods(["POST"])
def checkReplacement(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except JSONDecodeError:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    dirId = data.get('dirId', '').strip()
    fileName = data.get('fname', '').strip()
    return JsonResponse({
        "isFileExist": FileDAO.isFileExist(fileName, dirId, request.user),
        "fileId": FileDAO.getFileIdFromName(fileName, dirId, request.user)
    }, status=200)


@login_required
def download(request):
    fileId = request.GET.get("fid")
    key = request.GET.get("k")
    try:
        file = FileDAO.getFileFromId(fileId, request.user)
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)
    except FieldError:
        return JsonResponse({"message": "Bad input"}, status=400)

    try:
        file_data = FileSystemDAO.get_file(file.directory, file.id, key)
        response = HttpResponse(file_data, content_type=file.type)
        response['Content-Disposition'] = 'inline; filename*=UTF-8\'\'%s' % urllib.parse.quote(
            file.name.encode('utf-8'))
        return response
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Not found"}, status=404)


@csrf_exempt
@login_required
def test(request):
    # test API method
    # put your code here ok
    # user = request.user
    # fileKey = FileKeyDAO.getFileKey(user, file)
    # return JsonResponse({"message": "Executed"}, status=200)
    return share(request)


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
    fileId = data.get('fileId', '').strip()
    name = data.get('name', '').strip()
    if not fileId or not name:
        return JsonResponse({"message": "Bad input"}, status=400)

    try:
        file = FileDAO.getFileFromId(fileId, request.user)
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)
    except FieldError:
        return JsonResponse({"message": "Bad input"}, status=400)
    try:
        FileDAO.rename(file, name, request.user)
        return JsonResponse({"message": "Success"}, status=200)
    except (PermissionDenied, FileExistsError):
        return JsonResponse({"message": "Not found"}, status=404)


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


@login_required
@require_http_methods(["POST"])
def getFileKey(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except JSONDecodeError:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    fileId = data.get('fileId', '').strip()
    user = request.user
    try:
        fk = FileKeyDAO.getFileKey(user, fileId)
        return JsonResponse({"key": fk.key}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Not found"}, status=404)


@login_required
@require_http_methods(["POST"])
def removeFile(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except JSONDecodeError:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    fileId = data.get('fileId', '').strip()
    try:
        FileDAO.remove(fileId, request.user)
        return JsonResponse({"message": 'File removed'}, status=200)
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)


@login_required
@require_http_methods(["POST"])
def share(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except JSONDecodeError:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    elementId = data.get('elementId', '').strip()
    targetUserId = data.get('targetUserId', '').strip()
    key = data.get('encryptedKey', '').strip()  # Need only for file sharing| /!\ directory sharing don't handle FileKey
    read = data.get('read', 0)
    write = data.get('write', 0)
    share = data.get('share', 0)
    user = request.user

    # Input Check
    if is_uuid(elementId) and is_uuid(targetUserId):
        try:
            element = DirectoryDAO.getDirectoryFromId(elementId, user)
        except ObjectDoesNotExist:
            try:
                element = FileDAO.getFileFromId(elementId, user)
            except ObjectDoesNotExist:
                return JsonResponse({"message": "Not found"}, status=404)
        try:
            targetUser = UserDAO.getUserFromId(targetUserId)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Not found"}, status=404)

        if type(element) is File and key == "":
            return JsonResponse({"message": "Bad inputs"}, status=400)

        try:
            # TODO check is perm exist => then update
            PermissionDAO.share(user, targetUser, element, read, write, share)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=400)
        if type(element) is File:
            FileKeyDAO.insertFileKey(targetUser, element, key)
        return JsonResponse({"message": "Success"}, status=200)

    else:
        return JsonResponse({"message": "Bad inputs."}, status=400)


@login_required
def ls_shared(request):
    user = request.user
    dir_list = PermissionDAO.getSharedDirectory(user)
    file_list = PermissionDAO.getSharedFile(user)
    return JsonResponse({"directory": dir_list, "file": file_list}, status=200)
