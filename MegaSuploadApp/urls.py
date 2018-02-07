from django.urls import path
from MegaSuploadApp import views as app_view

urlpatterns = [
    path('', app_view.index, name="home"),
    path('index/', app_view.index, name="home"),
]
