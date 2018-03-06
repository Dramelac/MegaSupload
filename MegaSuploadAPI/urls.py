from django.urls import path

from MegaSuploadAPI.views import users_views, file_views

urlpatterns = [
    path('auth/register', users_views.register),
    path('auth/login', users_views.login),
    path('auth/logout', users_views.logout, name="logout"),
    path('user/update_profile', users_views.update_profile),
    path('file/upload', file_views.upload, name="upload"),
    path('file/download', file_views.download, name="download"),
    path('test', file_views.test),
]
