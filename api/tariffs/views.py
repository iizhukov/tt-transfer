from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.address.models import City
from .models import (
    IntracityTariff, PriceToCarClass,
    ServiceToPrice, ZoneToPrice
)
from .serializer import (
    IntracityTariffSerializer
)


class IntracityTariffView(APIView):
    serializer_class = IntracityTariffSerializer

    def get(self, request):
        region_ = request.query_params.get("region")
        city_ = request.query_params.get("city")

        city = get_object_or_404(
            City,
            region=region_,
            city=city_
        )

        tariffs = IntracityTariff.objects.filter(
            city=city
        )

        serializer = self.serializer_class(
            tariffs,
            many=True
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )
    
    def post(self, request):
        pass