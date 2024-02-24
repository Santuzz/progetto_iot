from rest_framework import serializers

from .models import *

# you can create multiple serializer, the important is they have different class name


class WebcamSerializer(serializers.ModelSerializer):
    crossroad = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Webcam
        fields = [
            'cars_count',
            'active',
            'crossroad'
        ]

    def get_crossroad(self, obj):
        print(obj.crossroad)
        if not isinstance(obj, Webcam) or obj.crossroad is None:
            return None
        return Crossroad.objects.get(id=obj.crossroad).name


class CrossroadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crossroad
        fields = [
            'name',
            'latitude',
            'longitude',
            'active',
            'creation_date',
            'traffic_level'
        ]
