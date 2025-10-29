# MapApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview_map_view, name='index'),
    path('OlPejeta/', views.olpejeta, name='olpejeta'),
    path('OlPejeta/Flight_Cylinders/', views.flight_cylinders, name='flight_cylinders'),
    path('OlPejeta/UTM/', views.utm_view, name='utm'),
    path('OlPejeta/utm_map_view/', views.utm_map_view, name='utm_map_view'),
    path('OlPejeta/overview/', views.overview_map_view, name='overview_map'),
    path('OlPejeta/operation_request/', views.operation_request, name='operation_request'), 
]