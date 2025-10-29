from django.db import models
from shared.constants import OPERATION_TYPE_CHOICES, DRONE_PLATFORM_CHOICES, NUMBER_OF_DRONES_CHOICES

class Procedure(models.Model):
    operation_type = models.CharField(max_length=20, choices=OPERATION_TYPE_CHOICES, default='VLOS')
    drone_platform = models.CharField(max_length=20, choices=DRONE_PLATFORM_CHOICES, default='DJI')
    number_of_drones = models.CharField(max_length=20, choices=NUMBER_OF_DRONES_CHOICES, default='SINGLE')

    def __str__(self):
        return f"{self.operation_type} - {self.drone_platform}"