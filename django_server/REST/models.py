from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.contrib.postgres.fields import ArrayField
# from geopy.distance import geodesic


class Crossroad(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    cars_count = models.CharField(max_length=100, default="0,0,0,0")
    last_send = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    creation_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    traffic_level = models.FloatField(default=0)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    def get_list_count(self):
        return [int(x) for x in self.cars_count.split(',')]


class Street(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    length = models.IntegerField(default=100)
    alert = models.BooleanField(default=False)
    crossroad = models.ManyToManyField(Crossroad, through='StreetCrossroad', blank=True)


class StreetCrossroad(models.Model):
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    crossroad = models.ForeignKey(Crossroad, on_delete=models.CASCADE)
    cars = models.IntegerField(default=0)
    index = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Per assegnare il valore di index sulla base delle relazioni già esistenti per un determinato crossroad
        if not self.pk:
            current_count = StreetCrossroad.objects.filter(crossroad=self.crossroad).count()
            self.index = current_count
        super().save(*args, **kwargs)


class Webcam(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=False)
    crossroad = models.OneToOneField(Crossroad, on_delete=models.CASCADE, null=True, blank=True)


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
    crossroad = models.ForeignKey(Crossroad, on_delete=models.CASCADE, null=True, blank=True)
    street = models.ForeignKey(Street, on_delete=models.CASCADE, null=True, blank=True)

# TODO Sensore del particolato per la rilevazione della qualità dell'aria
