from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.contrib.postgres.fields import ArrayField
# from geopy.distance import geodesic


class Crossroad(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    creation_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    traffic_level = models.FloatField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Street(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    length = models.IntegerField(default=100)
    alert = models.BooleanField(default=False)
    Crossroad = models.ManyToManyField(Crossroad, blank=True)


class Webcam(models.Model):
    id = models.AutoField(primary_key=True)
    cars_count = models.CharField(max_length=100, default="0,0,0,0")
    last_send = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    active = models.BooleanField(default=False)
    crossroad = models.OneToOneField(
        Crossroad, on_delete=models.CASCADE, null=True, blank=True)

    def get_list_count(self):
        return self.cars_count.split(',')


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
    green_value = models.FloatField(default=0.5)
    crossroad = models.ForeignKey(
        Crossroad, on_delete=models.CASCADE, null=True, blank=True)
    street = models.ForeignKey(
        Street, on_delete=models.CASCADE, null=True, blank=True)

# TODO Sensore del particolato per la rilevazione della qualità dell'aria
