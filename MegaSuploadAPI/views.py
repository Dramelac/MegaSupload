from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

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
    if not username or not first_name or not last_name or not email or not psw1 or not psw2:
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


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")


# TODO Auth -> return token
# TODO User update refer to existing django users

# TODO GetList(CurrentPath = '/') -> return list of file and directory | Filter by permission

# TODO GetFileKey
# TODO GetFile(FileKey)

