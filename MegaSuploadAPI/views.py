from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from MegaSuploadAPI.DAL.FileSystemDAO import *
from MegaSuploadAPI.models import *

import re
import json

from Crypto.PublicKey import RSA


@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    username = data.get('username', '').strip()
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    email = data.get('email', '').strip()
    psw1 = data.get('psw1', '')
    psw2 = data.get('psw2', '')
    if not username or not email or not psw1 or not psw2:
        return JsonResponse({"message": "Please fill all fields."}, status=400)
    if psw1 != psw2:
        return JsonResponse({"message": "Passwords are different."}, status=400)
    try:
        User.objects.get(username=username)
        return JsonResponse({"message": "User already exist."}, status=400)
    except User.DoesNotExist:
        if re.compile(r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]+").match(email) is None:
            return JsonResponse({"message": "Email address is not valid."}, status=400)
        key = RSA.generate(2048)
        encrypted_priv_key = key.exportKey(passphrase=psw1, pkcs=8, protection="scryptAndAES128-CBC").decode("utf8")
        pub_key = key.publickey().exportKey().decode("utf8")
        User.objects.create_user(username=username, email=email, password=psw1, first_name=first_name,
                                 last_name=last_name, encrypted_priv_key=encrypted_priv_key, pub_key=pub_key)
        auth = authenticate(username=username, password=psw1)
        auth_login(request, auth)
        return JsonResponse({
            "message": "Registration successful.",
            "priv_key": key.exportKey().decode("utf8")
        }, status=200)


@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    username = data.get('username', '').strip()
    password = data.get('password', '')
    auth = authenticate(username=username, password=password)
    if auth is not None:
        user = User.objects.get(id=auth.id)
        try:
            key = RSA.import_key(user.encrypted_priv_key.encode("utf8"), passphrase=password)
        except:
            return JsonResponse({"message": "Private key decryption failed."}, status=500)
        auth_login(request, auth)
        return JsonResponse({
            "message": "Login successful.",
            "priv_key": key.exportKey().decode("utf8")
        }, status=200)
    else:
        return JsonResponse({"message": "Bad credentials."}, status=401)


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")


@login_required
@require_http_methods(["POST"])
def update_profile(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({"message": "Bad JSON."}, status=400)
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    email = data.get('email', '').strip()
    pwd = data.get('pwd', '')
    psw1 = data.get('psw1', '')
    psw2 = data.get('psw2', '')
    if not email:
        return JsonResponse({"message": "Please fill all fields."}, status=400)
    if pwd and psw1 != psw2:
        return JsonResponse({"message": "Password confirmation is different."}, status=400)
    if re.compile(r"^[a-z0-9._-]+@[a-z0-9._-]+\.[a-z]+").match(email) is None:
        return JsonResponse({"message": "Email address is not valid."}, status=400)

    try:
        current_user = request.user
        user = User.objects.get(username=current_user)
        if pwd:
            auth = authenticate(username=current_user.username, password=pwd)
            if auth is not None:
                user.set_password(pwd)
            else:
                return JsonResponse({"message": "Current password error."}, status=400)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return JsonResponse({
            "message": "Update successful."
        }, status=200)
    except User.DoesNotExist:
        return JsonResponse({"message": "User not found."}, status=400)


# TODO GetList(CurrentPath = '/') -> return list of file and directory | Filter by permission

# TODO GetFileKey
# TODO GetFile(FileKey)

@login_required
@require_http_methods(["POST"])
def upload(request):
    filekey = store_file("", None)
    return JsonResponse({"message": "Success."}, status=200)


@login_required
def download(request):
    try:
        data = get_file(None)
        return JsonResponse({"message": data}, status=200)
    except Exception:
        return JsonResponse({"message": "File not found"}, status=404)
