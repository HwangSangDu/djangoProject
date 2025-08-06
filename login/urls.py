from django.urls import path
from . import views

urlpatterns = [
    path('', views.logInfo, name='logInfo'),
    path('', views.index),
]