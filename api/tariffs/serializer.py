from rest_framework import serializers

from api.address.serializers import CitySerializer
from api.cars.models import CAR_CLASSES
from .models import (
    IntracityTariff, PriceToCarClass,
    ServiceToPrice, Tariff, IntercityTariff,
    HubToPrice, CityToPrice, GlobalAddressToPrice,
    CityToPrice, GlobalAddressToPrice,
    AdditionalHubZoneToPrice
)


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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["prices"] = sorted(
            response["prices"],
            key=lambda x: x["id"]
        )
        return response


class AdditionalHubzonePricesSerializer(serializers.ModelSerializer):
    prices = PriceToCarClassSerializer(many=True)

    class Meta:
        model = AdditionalHubZoneToPrice
        fields = "__all__"
        depth = 2

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["prices"] = sorted(
            response["prices"],
            key=lambda x: x["id"]
        )
        return response


class HubToPriceSerializer(serializers.ModelSerializer):
    prices = PriceToCarClassSerializer(many=True)
    additional_hubzone_prices = AdditionalHubzonePricesSerializer(many=True)

    class Meta:
        model = HubToPrice
        fields = "__all__"
        depth = 2

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["prices"] = sorted(
            response["prices"],
            key=lambda x: x["id"]
        )
        return response


class IntracityTariffSerializer(serializers.ModelSerializer):
    hub_to_prices = HubToPriceSerializer(many=True)

    class Meta:
        model = IntracityTariff
        fields = ("id", "hub_to_prices")
        depth = 3


class CityToPriceSerializer(serializers.ModelSerializer):
    prices = PriceToCarClassSerializer(many=True)

    class Meta:
        model = CityToPrice
        fields = "__all__"
        depth = 2

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["prices"] = sorted(
            response["prices"],
            key=lambda x: x["id"]
        )
        return response


class GlobalAddressToPriceSerializer(serializers.ModelSerializer):
    prices = PriceToCarClassSerializer(many=True)

    class Meta:
        model = GlobalAddressToPrice
        fields = "__all__"
        depth = 2

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["prices"] = sorted(
            response["prices"],
            key=lambda x: x["id"]
        )
        return response


class IntercityTariffSerializer(serializers.ModelSerializer):
    cities = CityToPriceSerializer(many=True)
    global_addresses = PriceToCarClassSerializer(many=True)

    class Meta:
        model = IntercityTariff
        fields = "__all__"
        depth = 3


class TariffSerializer(serializers.ModelSerializer):
    services = ServiceToPriceSerializer(many=True, read_only=True)
    intracity_tariff = IntracityTariffSerializer(read_only=True)
    intercity_tariff = IntercityTariffSerializer(read_only=True)

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
