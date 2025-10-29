from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_procedure, name='create_procedure'),
    path('download_zip/', views.download_zip, name='download_zip'),
]