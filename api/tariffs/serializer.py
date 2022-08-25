from rest_framework import serializers

from .models import (
    IntracityTariff, PriceToCarClass,
    ServiceToPrice
)


class IntracityTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntracityTariff
        fields = "__all__"
        depth = 2
