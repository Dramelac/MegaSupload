from django.urls import path

from MegaSuploadAPI.views import users_views, file_views

urlpatterns = [
    path('auth/register', users_views.register),
    path('auth/login', users_views.login),
    path('auth/logout', users_views.logout, name="logout"),
    path('user/update_profile', users_views.update_profile),
    path('user/ratio', users_views.get_ratio),
    path('file/upload', file_views.upload, name="upload"),
    path('file/download', file_views.download),
    path('file/list_item', file_views.ls),
    path('file/add_dir', file_views.addDirectory),
    path('file/rename_dir', file_views.renameDirectory),
    path('file/rename_file', file_views.renameFile),
    path('file/move_dir', file_views.moveDir),
    path('file/move_file', file_views.moveFile),
    path('file/check_file', file_views.checkReplacement),
    path('file/get_key', file_views.getFileKey),
    path('file/remove_file', file_views.removeFile),
    path('test', file_views.test),
]
