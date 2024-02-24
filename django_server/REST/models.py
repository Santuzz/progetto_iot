from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
# from geopy.distance import geodesic


class Crossroad(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
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
        Crossroad, on_delete=models.CASCADE, null=True)
    # per avere una sola webcam ad incrocio sostituire crossroad con il seguente field
    # crossroad = models.OneToOneField(
    #    Crossroad, on_delete=models.CASCADE, primary_key=True)

    def get_crossroad(self):
        crossroad = Crossroad.objects.get(id=self.crossroad.id).name
        return crossroad


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
        Crossroad, on_delete=models.CASCADE, null=True)

# TODO Sensore del particolato per la rilevazione della qualità dell'aria
