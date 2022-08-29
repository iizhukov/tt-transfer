from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.address.models import City
from .models import (
    IntracityTariff, PriceToCarClass,
    ServiceToPrice, Tariff
)
from .serializer import (
    IntracityTariffSerializer, TariffSerializer,
    SimpleTariffSerializer
)


class TariffView(APIView):
    serializer_class = TariffSerializer

    def get(self, request: Request, tariff_id: int = None):
        if tariff_id:
            return self.get_by_id(request, tariff_id)
        else:
            return self.get_list(request)

    def get_by_id(self, request: Request, tariff_id: int):
        serializer = self.serializer_class(
            get_object_or_404(
                Tariff,
                id=tariff_id
            )
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def get_list(self, request: Request):
        serializer = SimpleTariffSerializer(
            Tariff.objects.all(),
            many=True
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def post(self, request: Request):
        city = City.objects.get_or_create(
            region=request.data.get("region"),
            city=request.data.get("city")
        )[0]

        serializer = self.serializer_class(
            data={
                **request.data,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(city=city)
        
        return Response(
            serializer.data,
            status.HTTP_200_OK
        )


class TariffServicesView(APIView):
    pass


# class IntracityTariffView(APIView):
#     serializer_class = IntracityTariffSerializer

#     def get(self, request):
#         region_ = request.query_params.get("region")
#         city_ = request.query_params.get("city")

#         city = get_object_or_404(
#             City,
#             region=region_,
#             city=city_
#         )

#         tariffs = IntracityTariff.objects.filter(
#             city=city
#         )

#         serializer = self.serializer_class(
#             tariffs,
#             many=True
#         )

#         return Response(
#             serializer.data,
#             status.HTTP_200_OK
#         )
    
#     def post(self, request):
#         pass
