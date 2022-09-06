from typing import Dict, List
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.address.models import City, GlobalAddress
from .models import (
    IntracityTariff, PriceToCarClass,
    ServiceToPrice, Tariff,
    GlobalAddressToPrice, CityToPrice,
    DEFAULT_SERVICES_LIST,
    DEFAULT_SERVICES_ONLY_DRIVERS_LIST
)
from .serializer import (
    IntracityTariffSerializer, TariffSerializer,
    SimpleTariffSerializer, PriceToCarClassSerializer,
    CityToPriceSerializer, GlobalAddressToPriceSerializer
)
from api.address.serializers import (
    CitySerializer, GlobalAddressSerializer
)


SERVICES = [
    *DEFAULT_SERVICES_LIST,
    *DEFAULT_SERVICES_ONLY_DRIVERS_LIST
]


class TariffView(APIView):
    serializer_class = TariffSerializer

    def get(self, request: Request, tariff_id: int | None = None):
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

        print(serializer.instance.services)

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

    def put(self, request: Request, tariff_id: int):
        serializer = self.serializer_class(
            instance=get_object_or_404(
                Tariff,
                pk=tariff_id
            ),
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def delete(self, request: Request, tariff_id: int):
        tariff = get_object_or_404(
            Tariff,
            id=tariff_id
        )
        tariff.delete()

        return Response(
            {},
            status.HTTP_200_OK
        )


class PriceToCarClassView(APIView):
    serializer_class = PriceToCarClassSerializer

    def pust(self, request: Request, pk: int | None = None):
        if isinstance(pk, int):
            return self.put_by_id(request, pk)
        else:
            return self.put_many(request, pk)

    def put_by_id(self, request: Request, pk: int):
        serializer = self.serializer_class(
            instance=get_object_or_404(
                PriceToCarClass,
                pk=pk
            ),
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def put_many(self, request: Request):
        prices: List[Dict[str, str]] = request.data.getlist("prices")

        for price in prices:
            serializer = self.serializer_class(
                instance=PriceToCarClass.objects.filter(
                    pk=price.get("id")
                ).first(),
                data=price
            )
            if serializer.is_valid():
                serializer.save()
        
        return Response(
            {},
            status.HTTP_200_OK
        )


class AddLocationToTariff(APIView):
    location = None

    def post(self, request: Request, tariff_id: int):
        if self.location == "city":
            return self._post_for_city(request, tariff_id)
        
        if self.location == "global_address":
            return self._post_for_global_address(request, tariff_id)

        return Response(
            {
                "detail": "bad location"
            },
            status.HTTP_400_BAD_REQUEST
        )

    def _post_for_city(self, request: Request, tariff_id: int):
        tariff: Tariff = get_object_or_404(
            Tariff,
            pk=tariff_id
        )

        city_serializer = CitySerializer(
            data=request.data
        )
        city_serializer.is_valid(raise_exception=True)

        city = get_object_or_404(
            City,
            city=city_serializer.data.get("city"),
            region=city_serializer.data.get("region")
        )

        city_to_price = CityToPrice.objects.create(
            city=city
        )

        tariff.intercity_tariff.cities.add(city_to_price)

        serializer = TariffSerializer(
            tariff
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def _post_for_global_address(self, request: Request, tariff_id: int):
        tariff: Tariff = get_object_or_404(
            Tariff,
            pk=tariff_id
        )

        global_address = get_object_or_404(
            GlobalAddress,
            id=request.data.get("global_address_id")
        )
        
        global_address_to_price = GlobalAddressToPrice.objects.create(
            global_address=global_address
        )

        tariff.intercity_tariff.global_addresses.add(global_address_to_price)

        serializer = TariffSerializer(
            tariff
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def delete(self, request: Request, tariff_id: int, location_id: int):
        if self.location == "city":
            return self._delete_for_city(request, tariff_id, location_id)
        
        if self.location == "global_address":
            return self._delete_for_global_address(request, tariff_id, location_id)

        return Response(
            {
                "detail": "bad location"
            },
            status.HTTP_400_BAD_REQUEST
        )
    
    def _delete_for_city(self, request: Request, tariff_id: int, location_id: int):
        tariff: Tariff = get_object_or_404(
            Tariff,
            id=tariff_id
        )

        city_to_price: CityToPrice = get_object_or_404(
            tariff.intercity_tariff.cities,
            id=location_id
        )

        for price in city_to_price.prices.all():
            price.delete()
        
        city_to_price.delete()

        return Response(
            {},
            status.HTTP_200_OK
        )

    def _delete_for_global_address(self, request: Request, tariff_id: int, location_id: int):
        tariff: Tariff = get_object_or_404(
            Tariff,
            id=tariff_id
        )

        global_address_to_price: GlobalAddressToPrice = get_object_or_404(
            tariff.intercity_tariff.global_addresses,
            id=location_id
        )

        for price in global_address_to_price.prices.all():
            price.delete()

        global_address_to_price.delete()

        return Response(
            {},
            status.HTTP_200_OK
        )


class GetServicesView(APIView):
    def get(self, request: Request):
        response = []

        for ind, service in enumerate(SERVICES, 1):
            response.append({
                "id": ind,
                "title": service[0],
                "slug": service[1]
            })
        
        return Response(
            response,
            status.HTTP_200_OK
        )


class EditTariffPricesView(APIView):
    def put(self, request: Request, tariff_id: int):
        for price in request.data:
            to, id = price.split("-")
            price_to_car_class = PriceToCarClass.objects.get(
                pk=int(id)
            )

            if to == "driver":
                price_to_car_class.driver_price = request.data.get(price, 0)
            elif to == "customer":
                price_to_car_class.customer_price = request.data.get(price, 0)

            price_to_car_class.save()

        tariff = Tariff.objects.get(
            id=tariff_id
        )
        serializer = TariffSerializer(
            tariff
        )

        return Response(
            serializer.data,
            status.HTTP_201_CREATED
        )
