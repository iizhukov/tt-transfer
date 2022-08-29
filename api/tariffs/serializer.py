from rest_framework import serializers

from api.address.serializers import CitySerializer
from .models import (
    IntracityTariff, PriceToCarClass,
    ServiceToPrice, Tariff, IntercityTariff,
)


class IntracityTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntracityTariff
        fields = "__all__"
        depth = 2


class ServiceToPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceToPrice
        fields = ('service', 'prices', )
        depth = 1


class TariffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tariff
        fields = (
            'id', 'title', 'city', 'currency', 'comments',
            'is_commission', 'services',
            'intracity_tariff', 'intercity_tariff',
            'lifetime',
        )
        depth = 4


class SimpleTariffSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Tariff
        fields = (
            'name', 'city', 'currency', 'comments',
            'is_commission', 'lifetime'
        )
        depth = 1

# class TariffServicesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = 