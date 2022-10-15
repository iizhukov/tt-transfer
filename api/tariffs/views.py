from typing import Dict, List
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse
from django.conf import settings, Path
from django.shortcuts import get_object_or_404

from api.address.models import City, GlobalAddress, Hub
from api.profile.models import Company
from api.permissions import IsManagerOrAdminUser
from .models import (
    HubsToPriceModel, IntracityTariff, PriceToCarClass,
    ServiceToPrice, Tariff,
    GlobalAddressToPrice, CityToPrice,
    DEFAULT_SERVICES_LIST,
    DEFAULT_SERVICES_ONLY_DRIVERS_LIST
)
from .serializer import (
    IntracityTariffSerializer, TariffSerializer,
    SimpleTariffSerializer, PriceToCarClassSerializer,
    CityToPriceSerializer, GlobalAddressToPriceSerializer, IntercityTariffSerializer
)
from api.address.serializers import (
    CitySerializer, GlobalAddressSerializer
)
from api.smartFilter.filters import Filter
from api.excel import TariffToExcel


SERVICES = [
    *DEFAULT_SERVICES_LIST,
    *DEFAULT_SERVICES_ONLY_DRIVERS_LIST
]


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class SetLastUpdateTariff(APIView):
    def get(self, request, tariff_id: int):
        tariff = get_object_or_404(
            Tariff,
            pk=tariff_id
        )
        tariff.save()

        return Response(
            {},
            status.HTTP_200_OK
        )


class TariffView(APIView, BasicPagination):
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
        tariffs = Filter.tariffs(request.query_params)

        paginated = self.paginate_queryset(
            tariffs, request, view=self
        )
        serializer = SimpleTariffSerializer(paginated, many=True)
        response = self.get_paginated_response(serializer.data)

        return response

    def post(self, request: Request):
        city = get_object_or_404(
            City,
            region=request.data.get("region"),
            city=request.data.get("city")
        )

        serializer = self.serializer_class(
            data={
                **request.data,
            }
        )
        serializer.is_valid(raise_exception=True)

        if Tariff.objects.filter(
                city=city,
                type=serializer.validated_data.get("type"),
                commission=serializer.validated_data.get("commission")
        ):
            return Response(
                {
                    "detail": "Такой тариф уже существует"
                },
                status.HTTP_400_BAD_REQUEST
            )

        if serializer.validated_data.get("type") != "basic" and not Tariff.objects.filter(
                city=city,
                type="basic"
        ):
            return Response(
                {
                    "detail": "Нет основного тарифа для этого города"
                },
                status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("type") == "company":
            company = get_object_or_404(
                Company,
                pk=request.data.get("company")
            )
            tariff = serializer.save(city=city, company=company)
        else:
            tariff = serializer.save(city=city)

        short_tariff_serializer = SimpleTariffSerializer(
            tariff
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

        # return Response(
        #     {
        #         "tariff": serializer.data,
        #         "short_tariff": short_tariff_serializer.data,
        #     },
        #     status.HTTP_200_OK
        # )

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

        serializer = SimpleTariffSerializer(
            Tariff.objects.all(),
            many=True
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )


class PriceToCarClassView(APIView):
    serializer_class = PriceToCarClassSerializer

    def pust(self, request: Request, pk: int = None):
        if isinstance(pk, int):
            return self.put_by_id(request, pk)
        else:
            return self.put_many(request)

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
            price_ = PriceToCarClass.objects.filter(
                pk=price.get("id")
            ).first()
            print(price_, price)
            serializer = self.serializer_class(
                instance=price_,
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

        if self.location == "hub":
            return self._post_for_hub(request, tariff_id)

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

        if tariff.intercity_tariff.cities.filter(
                city=city
        ):
            return Response(
                {
                    "detail": "Город с таким именем уже задан"
                },
                status.HTTP_400_BAD_REQUEST
            )
            
        if city == tariff.city:
            return Response(
                {
                    "detail": "Вы не можете создать межгородское направление из города 'A' в город 'А'."
                },
                status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("converse", False) and not Tariff.objects.filter(
                city=city,
                type=tariff.type,
                commission=tariff.commission
        ):
            return Response(
                {
                    "detail": f"Для начала создайте тариф для города {city.city}"
                },
                status.HTTP_400_BAD_REQUEST
            )

        city_to_price = CityToPrice.objects.create(
            city=city,
            converse=request.data.get("converse", False)
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
            address=request.data.get("global_address")
        )

        if tariff.intercity_tariff.global_addresses.filter(
                global_address=global_address
        ):
            return Response(
                {
                    "detail": f"Маршрут для глобального адреса '{global_address}' уже создан."
                },
                status.HTTP_400_BAD_REQUEST
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

    def _post_for_hub(self, request: Request, tariff_id: int):
        tariff: Tariff = get_object_or_404(
            Tariff,
            pk=tariff_id
        )

        hub = get_object_or_404(
            Hub,
            title=request.data.get("hub")
        )
        
        if tariff.intercity_tariff.hubs.filter(
                hub=hub
        ):
            return Response(
                {
                    "detail": f"Маршрут для хаба '{hub.title}' уже создан."
                },
                status.HTTP_400_BAD_REQUEST
            )

        hub_to_price = HubsToPriceModel.objects.create(
            hub=hub
        )

        tariff.intercity_tariff.hubs.add(hub_to_price)

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

        if self.location == "hub":
            return self._delete_for_hub(request, tariff_id, location_id)

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
            tariff.intercity_tariff.cities.all(),
            id=location_id
        )
        
        if city_to_price.converse:
            tariff_: Tariff = Tariff.objects.get(
                city=city_to_price.city,
                type=tariff.type,
                commission=tariff.commission
            )
            city_to_price2 = tariff_.intercity_tariff.cities.get(
                city=tariff.city
            )

            city_to_price2.delete()

        city_to_price.delete()

        serializer = IntercityTariffSerializer(
            tariff.intercity_tariff
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def _delete_for_global_address(self, request: Request, tariff_id: int, location_id: int):
        tariff: Tariff = get_object_or_404(
            Tariff,
            id=tariff_id
        )

        global_address_to_price: GlobalAddressToPrice = get_object_or_404(
            tariff.intercity_tariff.global_addresses.all(),
            id=location_id
        )

        global_address_to_price.delete()

        serializer = IntercityTariffSerializer(
            tariff.intercity_tariff
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def _delete_for_hub(self, request: Request, tariff_id: int, location_id: int):
        tariff: Tariff = get_object_or_404(
            Tariff,
            id=tariff_id
        )

        hub_to_price: HubsToPriceModel = get_object_or_404(
            tariff.intercity_tariff.hubs.all(),
            id=location_id
        )

        hub_to_price.delete()

        serializer = IntercityTariffSerializer(
            tariff.intercity_tariff
        )

        return Response(
            serializer.data,
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


class ExportTariffView(APIView):
    permission_classes = (IsManagerOrAdminUser,)

    def get(self, request: Request):
        tariff_ids = request.query_params.getlist("tariffs")

        filename = TariffToExcel.export(
            (
                Tariff.objects.filter(
                    pk__in=tariff_ids
                )

                if tariff_ids else

                Tariff.objects.all()
            ).order_by("-id")
        )

        url = Path(
            settings.EXCEL_ROOT,
            "tariffs/",
            filename
        )

        with open(url, "rb") as excel:
            response = HttpResponse(
                excel.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['filename'] = filename
            return response


class TariffSearchView(APIView):
    class_serializer = SimpleTariffSerializer

    def get(self, request: Request):
        search = request.query_params.get("search")
        
        if not search:
            return Response(
                [],
                status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.class_serializer(
            Tariff.search_by_string(search.strip().lower()),
            many=True
        )
        
        return Response(
            serializer.data,
            status.HTTP_200_OK
        )
