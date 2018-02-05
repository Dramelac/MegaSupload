from django.urls import path
from MegaSuploadApp import views

urlpatterns = [
    path('', views.index, name='index'),
]