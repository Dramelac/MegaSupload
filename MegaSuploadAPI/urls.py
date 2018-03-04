from django.urls import path
from MegaSuploadAPI import views as app_view

urlpatterns = [
    path('auth/register', app_view.register),
    path('auth/login', app_view.login),
    path('auth/logout', app_view.logout, name="logout"),
]
