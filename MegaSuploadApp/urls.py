from django.urls import path
from MegaSuploadApp import views as app_view

urlpatterns = [
    path('', app_view.index, name="home"),
    path('index/', app_view.index, name="home"),
    path('login/', app_view.login, name="login"),
    path('register/', app_view.register, name="register"),
    path('profile/', app_view.profile, name="profile")
]
