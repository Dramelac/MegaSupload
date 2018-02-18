from django.urls import path
from MegaSuploadAPI import views as app_view

urlpatterns = [
    path('', app_view.index, name="home"),
]
