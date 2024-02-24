from django.contrib import admin
from .models import *
# Register your models here.


class WebcamAdmin(admin.ModelAdmin):
    list_display = ('id', 'cars_count', 'active', 'crossroad')


class CrossroadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'latitude', 'longitude',
                    'traffic_level', 'active')


admin.site.register(Webcam)
admin.site.register(Crossroad)
admin.site.register(Trafficlight)
