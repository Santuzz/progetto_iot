from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
# from geopy.distance import geodesic

# TODO mettere il nome come chiave primaria


class Crossroad(models.Model):
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    creation_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    traffic_level = models.FloatField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Webcam(models.Model):
    id = models.AutoField(primary_key=True)
    cars_count = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    crossroad = models.ForeignKey(
        Crossroad, on_delete=models.CASCADE, null=True, blank=True)


class Trafficlight(models.Model):
    DIRECTION_CHOICES = [
        ('LS', 'Left straight'),
        ('L', 'Left'),
        ('RS', 'Right straight'),
        ('R', 'Right'),
        ('A', 'Any'),
        ('S', 'Straight')
    ]
    id = models.AutoField(primary_key=True)
    direction = models.CharField(choices=DIRECTION_CHOICES, max_length=100)
    green_probability = models.FloatField(default=0.5)
    crossroad = models.ForeignKey(
        Crossroad, on_delete=models.CASCADE, null=True, blank=True)

# TODO Sensore del particolato per la rilevazione della qualità dell'aria
