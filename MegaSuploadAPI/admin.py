from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Permission)
admin.site.register(Directory)
admin.site.register(File)
admin.site.register(FileKey)
