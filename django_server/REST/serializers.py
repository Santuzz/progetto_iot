from rest_framework import serializers

from .models import *

# you can create multiple serializer, the important is they have different class name


class WebcamSerializer(serializers.ModelSerializer):
    crossroad_name = serializers.CharField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Webcam
        fields = [
            'id',
            # 'cars_count',
            'active',
            'crossroad_name'
        ]

    def create(self, validated_data):
        crossroad_data = None

        try:
            crossroad_data = validated_data.pop('crossroad_name')
        except KeyError:
            pass
        instance = Webcam.objects.create(**validated_data)

        if crossroad_data is not None:
            instance.crossroad = Crossroad.objects.get(name=crossroad_data)
        else:
            instance.crossroad = None
        instance.save()

        return instance


"""
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


class TrafficlightSerializer(serializers.ModelSerializer):

    crossroad_name = serializers.CharField(
        write_only=True, required=False, allow_null=True)
    street_name = serializers.CharField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Trafficlight
        fields = [
            'id',
            'direction',
            'green_value',
            'crossroad_name',
            'street_name'
        ]

    def create(self, validated_data):
        crossroad_data = None
        street_data = None

        try:
            crossroad_data = validated_data.pop('crossroad_name')
            street_data = validated_data.pop('street name')
        except KeyError:
            pass
        instance = Trafficlight.objects.create(**validated_data)

        if crossroad_data is not None:
            instance.crossroad = Crossroad.objects.get(name=crossroad_data)
        else:
            instance.crossroad = None

        if street_data is not None:
            instance.street = Crossroad.objects.get(name=street_data)
        else:
            instance.street = None

        instance.save()

        return instance

    def update(self, instance, validated_data):
        try:
            crossroad_data = validated_data.pop('crossroad_name')
            street_data = validated_data.pop('street name')

            if crossroad_data is not None:
                instance.crossroad = Crossroad.objects.get(name=crossroad_data)
            else:
                instance.crossroad = None

            if street_data is not None:
                instance.street = Crossroad.objects.get(name=street_data)
            else:
                instance.street = None
        except KeyError:
            pass

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance


class CrossroadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crossroad
        fields = [
            'name',
            'latitude',
            'longitude',
            'active',
            'creation_date',
            'traffic_level',
            'last_send',
            'cars_count'
        ]
    """
    def update(self, instance, validated_data):
        try:
            crossroad_data = validated_data.pop('name')

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


class StreetSerializer(serializers.ModelSerializer):

    crossroad_name = serializers.CharField(
        write_only=True, required=False, allow_null=True)

    class Meta:
        model = Street
        fields = [
            'name',
            'length',
            'alert',
            'crossroad_name'
        ]

    def create(self, validated_data):
        crossroad_data = None

        try:
            crossroad_data = validated_data.pop('crossroad_name')
        except KeyError:
            pass
        instance = Street.objects.create(**validated_data)

        if crossroad_data is not None:
            instance.crossroad = Crossroad.objects.get(name=crossroad_data)
        else:
            instance.crossroad = None
        instance.save()

        return instance

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
