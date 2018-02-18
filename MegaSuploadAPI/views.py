from django.http import HttpResponse
from django.shortcuts import render

# Prefer using JSON

def index(request):
    return HttpResponse("It works !")

# TODO Auth -> return token
# TODO User update refer to existing django users

# TODO GetList(CurrentPath = '/') -> return list of file and directory | Filter by permission

# TODO GetFileKey
# TODO GetFile(FileKey)

