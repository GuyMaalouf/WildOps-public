from django.urls import path
from .views import weather_check

urlpatterns = [
    path('', weather_check, name='weather_check'),
]