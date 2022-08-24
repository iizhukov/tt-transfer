from rest_framework import serializers

from . import models


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = "__all__"
        depth = 1


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"
        depth = 2


class AddAddressSerializer(serializers.Serializer):
    country = serializers.CharField()
    region = serializers.CharField(allow_null=True)
    city = serializers.CharField()
    street = serializers.CharField()
    number = serializers.CharField()

    class Meta:
        fields = ('country', 'region', 'city', 'street', 'number')


class CityZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CityZone
        fields = "__all__"
        depth = 2


class GetZoneByCoordsSerializer(serializers.Serializer):
    region = serializers.CharField()
    city = serializers.CharField()
    address_latitude = serializers.FloatField()
    address_longitude = serializers.FloatField()

    class Meta:
        fields = "__all__"
        depth = 1


class HubSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hub
        fields = "__all__"
        depth = 2


class HubZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HubZone
        fields = "__all__"
        depth = 2


class GetZoneByAddressSerializer(serializers.Serializer):
    pass