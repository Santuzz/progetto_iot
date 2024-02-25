from rest_framework import serializers

from .models import *

# you can create multiple serializer, the important is they have different class name


class WebcamSerializer(serializers.ModelSerializer):
    crossroad = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Webcam
        fields = [
            'id',
            'cars_count',
            'active',
            'crossroad'
        ]

    def get_crossroad(self, obj):
        if not isinstance(obj, Webcam) or obj.crossroad is None:
            return None
        return Crossroad.objects.get(name=obj.crossroad).id


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
