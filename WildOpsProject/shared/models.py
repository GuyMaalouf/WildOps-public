from django.db import models

class OperationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class DronePlatform(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name