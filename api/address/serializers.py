from rest_framework import serializers

from . import models


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = "__all__"
        depth = 1


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
        fields = ('city', 'color', 'coordinates')
        depth = 1
