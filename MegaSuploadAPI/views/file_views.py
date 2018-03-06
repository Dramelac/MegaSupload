from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied, FieldError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from MegaSuploadAPI.DAL import FileSystemDAO, DirectoryDAO
from MegaSuploadAPI.forms import *


@login_required
@require_http_methods(["POST"])
def upload(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        file = request.FILES['file']
        FileSystemDAO.store_file("/" + request.user.username + "/", file)
        return JsonResponse({"message": "Success."}, status=200)
    return JsonResponse({"message": "Error invalid input."}, status=400)


@login_required
def download(request):
    dirId = request.GET.get("did")
    fileId = request.GET.get("fid")
    try:
        directory = DirectoryDAO.getDirectoryFromId(dirId, request.user)
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)
    except FieldError:
        return JsonResponse({"message": "Bad input"}, status=400)

    # TODO add file DAO
    try:
        file = FileSystemDAO.get_file(directory, fileId, "")
        response = HttpResponse(file, content_type="text/plain")
        response['Content-Disposition'] = 'inline; filename=' + fileId
        return response
    except ObjectDoesNotExist:
        return JsonResponse({"message": "File not found"}, status=404)


@login_required
def downloadPath(request):
    path = request.GET.get("path")
    file = request.GET.get("file")
    try:
        directory = DirectoryDAO.getDirectoryFromPath(path, request.user)
    except (ObjectDoesNotExist, PermissionDenied):
        return JsonResponse({"message": "Not found"}, status=404)
    except FieldError:
        return JsonResponse({"message": "Bad input"}, status=400)

    # TODO add file DAO
    try:
        file = FileSystemDAO.get_file(directory, file, "")
        response = HttpResponse(file, content_type="text/plain")
        response['Content-Disposition'] = 'inline; filename=' + file
        return response
    except ObjectDoesNotExist:
        return JsonResponse({"message": "File not found"}, status=404)


@csrf_exempt
@login_required
def test(request):
    # test API method
    pass

# TODO GetList(CurrentPath = '/') -> return list of file and directory | Filter by permission

# TODO GetFileKey
# TODO GetFile(FileKey)
