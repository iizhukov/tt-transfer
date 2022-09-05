from rest_framework import serializers

from api.address.serializers import CitySerializer
from api.cars.models import CAR_CLASSES
from .models import (
    IntracityTariff, PriceToCarClass,
    ServiceToPrice, Tariff, IntercityTariff,
    CityToPrice, GlobalAddressToPrice
)


class IntracityTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntracityTariff
        fields = "__all__"
        depth = 2


class PriceToCarClassSerializer(serializers.ModelSerializer):
    car_class = serializers.CharField(read_only=True)
    ru_car_class = serializers.SerializerMethodField()

    class Meta:
        model = PriceToCarClass
        fields = (
            'id', 'car_class', 'ru_car_class', 'customer_price', 'driver_price'
        )

    def get_ru_car_class(self, obj: PriceToCarClass):
        return list(filter(
            lambda class_: class_[0] == obj.car_class,
            CAR_CLASSES
        ))[0][1]


class ServiceToPriceSerializer(serializers.ModelSerializer):
    prices = PriceToCarClassSerializer(many=True)

    class Meta:
        model = ServiceToPrice
        fields = ('title', 'slug', 'prices', )
        depth = 1


class TariffSerializer(serializers.ModelSerializer):
    services = ServiceToPriceSerializer(many=True, read_only=True)

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
            'id', 'title', 'city', 'currency', 'comments',
            'is_commission', 'lifetime'
        )
        depth = 1


class CityToPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityToPrice
        fields = "__all__"


class GlobalAddressToPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalAddressToPrice
        fields = "__all__"
