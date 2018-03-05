from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


@login_required(login_url="/app/login")
def profile(request):
    return render(request, 'user_profile.html')


@login_required
def upload(request):
    return render(request, 'upload.html')
