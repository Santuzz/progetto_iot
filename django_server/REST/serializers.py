from rest_framework import serializers

from .models import *

# you can create multiple serializer, the important is they have different class name


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


class WebcamSerializer(serializers.ModelSerializer):
    # crossroad = serializers.SerializerMethodField(read_only=True)
    # crossroad = CrossroadSerializer()
    # crossroad = serializers.PrimaryKeyRelatedField(
    #     queryset=Crossroad.objects.all())
    crossroad_name = serializers.CharField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Webcam
        fields = [
            'id',
            'cars_count',
            'active',
            'crossroad_name'
        ]

    def update(self, instance, validated_data):
        try:
            crossroad_data = validated_data.pop('crossroad_name')
            if crossroad_data is not None:
                instance.crossroad = Crossroad.objects.get(name=crossroad_data)
            else:
                instance.crossroad = None
        except KeyError:
            pass
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    """
    def create(self, validated_data):
        crossroad_data = validated_data.pop('crossroad')
        crossroad = Crossroad.objects.create(**crossroad_data)
        webcam = Webcam.objects.create(
            crossroad=crossroad, **validated_data)
        return webcam

    def update(self, instance, validated_data):
        crossroad_data = validated_data.pop('crossroad')
        if crossroad_data is not None:
            crossroad = instance.crossroad
            crossroad_serializer = CrossroadSerializer(
                crossroad, data=crossroad_data, partial=True)
            if crossroad_serializer.is_valid():
                crossroad_serializer.save()

        instance = super().update(instance, validated_data)
        return instance
    """
