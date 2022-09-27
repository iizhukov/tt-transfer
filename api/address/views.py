from typing import List
from django.forms import model_to_dict
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from shapely.geometry import Point, Polygon
from django.shortcuts import get_object_or_404
from fuzzywuzzy import fuzz

from .models import (
    Address, City, CityZone,
    Coordinate, Hub, HubZone,
    GlobalAddress
)
from .serializers import (
    CitySerializer, AddressSerializer,
    AddAddressSerializer, CityZoneSerializer,
    GetZoneByCoordsSerializer,
    HubSerializer, HubZoneSerializer,
    GlobalAddressSerializer
)
from api.tariffs.models import Tariff, AdditionalHubZoneToPrice
from api.request import DistanceAndDuration


REGIONS = set(City.objects.values_list('region', flat=True))
CITIES = {
    region: set(City.objects.filter(
        region=region
    ).values_list("city", flat=True))
    for region in REGIONS
}


class CityView(APIView):
    serializer_class = CitySerializer

    def get(self, request: Request):
        serializer = self.serializer_class(
            data=City.objects.all(),
            many=True,
        )
        serializer.is_valid()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request):
        serializer = self.serializer_class(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {"detail": "Данные невалидны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        city, created = City.objects.get_or_create(
            city=serializer.data.get("city"),
            region=serializer.data.get("region")
        )

        serializer = self.serializer_class(
            instance=city
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class AddressView(APIView):
    serializer_class = AddressSerializer

    def get(self, request: Request):
        serializer = self.serializer_class(
            Address.objects.all(),
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class AddAddressView(APIView):
    serializer_class = AddAddressSerializer

    def post(self, request: Request):
        if not self.serializer_class(data=request.data).is_valid():
            return Response(
                {"detail": "Некорректные данные"},
                status.HTTP_400_BAD_REQUEST
            )
        
        city_serializer = CitySerializer(data=request.data)
        city_serializer.is_valid()

        city = get_object_or_404(
            City,
            region=city_serializer.validated_data.get('region'),
            city=city_serializer.validated_data.get('city')
        )

        address = Address(
            city=city,
            street=request.data.get("street"),
            number=request.data.get("number")
        )
        address.save()

        address_serializer = AddressSerializer(
            instance=address
        )

        return Response(
            address_serializer.data,
            status.HTTP_200_OK
        )


class ZonesView(APIView):
    serializer_class = CityZoneSerializer
    permission_classes = (AllowAny, )
    
    def get(self, request: Request):
        city_ = request.query_params.get("city")
        region_ = request.query_params.get("region")

        city = get_object_or_404(
            City,
            region=region_,
            city=city_
        )

        serializer = self.serializer_class(
            data=CityZone.objects.filter(
                city=city
            ),
            many=True
        )
        serializer.is_valid()

        for ind, zone in enumerate(serializer.data):
            coordinates = []

            for coords in zone["coordinates"]:
                coordinates.append([coords["latitude"], coords["longitude"]])

            serializer.data[ind]["coordinates"] = [coordinates]

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def post(self, request: Request):
        city = get_object_or_404(
            City,
            region=request.data.get("region"),
            city=request.data.get("city")
        )

        zone = CityZone(
            city=city,
            color=request.data.get("color")
        )
        zone.save()

        coordinates = request.data.get("coordinates")[0]

        for latitude, longitude in coordinates:
            print(latitude, longitude)
            coords, created = Coordinate.objects.get_or_create(
                latitude=latitude,
                longitude=longitude
            )

            if created:
                coords.save()

            zone.coordinates.add(coords)

        serializer = CityZoneSerializer(
            instance=zone
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )


class EditZoneView(APIView):
    serializer_class = CityZoneSerializer

    def get(self, reqeust: Request, id: int):
        zone = get_object_or_404(CityZone, id=id)

        serializer = self.serializer_class(
            instance=zone
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def put(self, request: Request, id: int):
        zone = get_object_or_404(
            CityZone,
            pk=id
        )

        zone.color = request.data.get("color") or zone.color
        new_coords = request.data.get("coordinates")[0]

        if new_coords:
            zone.coordinates.clear()

            for latitude, longitude in new_coords:
                print(latitude, longitude)
                coords, _ = Coordinate.objects.get_or_create(
                    latitude=latitude,
                    longitude=longitude
                )

                zone.coordinates.add(coords)

        zone.save()

        serializer = self.serializer_class(
            instance=zone
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def delete(self, request: Request, id: int):
        zone = get_object_or_404(CityZone, id=id)

        zone.delete()

        return Response(
            {"detail": "deleted"},
            status.HTTP_200_OK
        )


class GetZoneByCoordsView(APIView):
    serializer_class = GetZoneByCoordsSerializer

    def post(self, request: Request):
        serializer = self.serializer_class(
            data=request.data
        )
        serializer.is_valid()

        if not serializer.is_valid():
            return Response(
                {"detail": "Данные не валидны"},
                status.HTTP_200_OK
            )

        city = get_object_or_404(
            City,
            region=serializer.data.get("region"),
            city=serializer.data.get("city")
        )
    
        zones = CityZone.objects.filter(
            city=city
        )

        address_point = Point(
            serializer.data.get("address_latitude"),
            serializer.data.get("address_longitude")
        )
        
        for zone in zones:
            coords = []

            for coord in zone.coordinates.all():
                coords.append(coord.get_tuple())

            zone_polygon = Polygon(
                coords
            )

            if zone_polygon.contains(address_point):
                zone_serializer = CityZoneSerializer(
                    instance=zone
                )

                return Response(
                    zone_serializer.data,
                    status.HTTP_200_OK
                )
        
        return Response(
            {},
            status.HTTP_200_OK
        )


class GetCityCenter(APIView):
    def get(self, request: Request):
        region_ = request.query_params.get("region")
        city_ = request.query_params.get("city")

        city = City.objects.get_or_create(
            region=region_,
            city=city_
        )[0]

        latitude = city.center.latitude
        longitude = city.canter.longitude

        return Response(
            {
                "latitude": latitude,
                "longitude": longitude
            },
            status.HTTP_200_OK
        )


class HubView(APIView):
    serializer_class = HubSerializer
    permission_classes = (AllowAny, )

    def get(self, request: Request):
        region_ = request.query_params.get("region")
        city_ = request.query_params.get("city")

        city = get_object_or_404(
            City,
            region=region_,
            city=city_
        )

        hubs = Hub.objects.filter(
            city=city
        )

        hubs_serializer = self.serializer_class(
            instance=hubs,
            many=True
        )
        city_serializer = CitySerializer(
            city
        )

        response = {
            "hubs": hubs_serializer.data,
            "city": city_serializer.data
        }

        return Response(
            response,
            status.HTTP_200_OK
        )

    def post(self, request: Request):
        region_ = request.data.get("region")
        city_ = request.data.get("city")

        lat, lon = request.data.get("coordinates")

        if not region_ or not city_:
            return Response(
                {"detail": "city or region is empty"},
                status.HTTP_400_BAD_REQUEST
            )

        if not lat or not lon:
            return Response(
                {"detail": "coordinates is empty"},
                status.HTTP_400_BAD_REQUEST
            )

        city = City.objects.get_or_create(
            region=region_,
            city=city_
        )[0]

        coordinates = Coordinate.objects.get_or_create(
            latitude=lat,
            longitude=lon
        )[0]

        serializer = self.serializer_class(
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST
            )
        
        instance = serializer.save(city=city, coordinate=coordinates)

        self._add_to_tariff(city, instance)

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def _add_to_tariff(self, city: City, instance):
        tariffs: List[Tariff] = Tariff.objects.filter(
            city=city
        )

        for tariff in tariffs:
            tariff._set_hub_prices([instance])


class HubZoneView(APIView):
    serializer_class = HubZoneSerializer

    def get(self, request: Request, hub_id: int):
        hub = get_object_or_404(
            Hub,
            id=hub_id
        )

        zones: List[HubZone] = HubZone.objects.filter(
            hub=hub
        )

        response = []

        for ind, zone in enumerate(zones):
            response.append(model_to_dict(zone))
            response[ind]["coordinates"] = zone.get_coordinates_as_list()

        return Response(
            response,
            status.HTTP_200_OK
        )

    def post(self, request: Request, hub_id: int):
        hub = get_object_or_404(
            Hub,
            id=hub_id
        )

        zone = HubZone(
            hub=hub,
            color=request.data.get("color"),
            title=request.data.get("title") or ""
        )

        instance = zone.save(request.data.get("coordinates")[0])
        self._add_to_tariffs(hub, instance)

        serializer = self.serializer_class(
            zone
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def _add_to_tariffs(self, hub, instance):
        print(instance)

        tariffs: List[Tariff] = Tariff.objects.filter(
            city=hub.city
        )

        for tariff in tariffs:
            for hub_to_price in tariff.intracity_tariff.hub_to_prices.all():
                if hub_to_price.hub == hub:
                    hub_to_price.additional_hubzone_prices.add(
                        AdditionalHubZoneToPrice.objects.create(
                            zone=instance
                        )
                    )


class EditHubZoneView(APIView):
    serializer_class = HubZoneSerializer

    def put(self, request: Request, zone_id: int):
        zone = get_object_or_404(
            HubZone,
            id=zone_id
        )
        hub = zone.hub

        zone.color = request.data.get("color") or zone.color
        zone.save(
            request.data.get("coordinates")[0]
        )

        zones: List[HubZone] = HubZone.objects.filter(
            hub=hub
        )

        response = []

        for ind, zone in enumerate(zones):
            response.append(model_to_dict(zone))
            response[ind]["coordinates"] = zone.get_coordinates_as_list()

        return Response(
            response,
            status.HTTP_200_OK
        )

    def delete(self, request: Request, zone_id: int):
        zone = get_object_or_404(
            HubZone,
            id=zone_id
        )
        zone.delete()

        return Response(
            {"detail": "Deleted"},
            status.HTTP_200_OK
        )


class GetHubZoneByCoordsAndHubView(APIView):
    def get(self, request: Request):
        latitude = float(request.query_params.get("latitude").replace(",", "."))
        longitude = float(request.query_params.get("longitude").replace(",", "."))

        hub = get_object_or_404(
            Hub,
            id=request.qeury_params.get("hub_id")
        )
        zones: List[HubZone] = HubZone.objects.filter(
            hub=hub
        )

        coords_point = Point(
            latitude,
            longitude
        )

        for zone in zones:
            zone_polygon = Polygon(
                zone.get_coordinates_as_list()
            )

            if zone_polygon.contains(coords_point):
                zone_serializer = CityZoneSerializer(
                    instance=zone
                )

                return Response(
                    zone_serializer.data,
                    status.HTTP_200_OK
                )

        return Response(
            {
                "detail": "Zone not found"
            },
            status.HTTP_400_BAD_REQUEST
        )


class GlobalAddressView(APIView):
    serializer_class = GlobalAddressSerializer

    def get(self, request: Request):
        serializer = self.serializer_class(
            GlobalAddress.objects.all(),
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
        )


class GetDistanceAndDurationBetweenCitiesView(APIView):
    def get(self, request: Request):
        regions = request.query_params.getlist("region")
        cities = request.query_params.getlist("city")

        cities_: List[City] = []
        for i in range(len(regions)):
            cities_.append(
                City.objects.get_or_create(
                    region=regions[i],
                    city=cities[i]
                )[0]
            )

        print(cities_)

        distance, hours, minutes = DistanceAndDuration.get(
            cities_[0].get_center_as_string(),
            cities_[-1].get_center_as_string(),
            [cities_[i].get_center_as_string() for i in range(1, len(cities_) - 1)]
        )

        return Response(
            {
                "distance": distance,
                "hours": hours,
                "minutes": minutes
            },
            status.HTTP_200_OK
        )


class FilterRegionsView(APIView):
    def get(self, request: Request):
        search = request.query_params.get("search")

        response = []

        if not search:
            return Response(
                [],
                status.HTTP_200_OK
            )

        for region in REGIONS:
            coincidence = fuzz.ratio(search.lower(), region.lower())
            response.append((region, coincidence))

            if coincidence == 100:
                return Response(
                    [region],
                    status.HTTP_200_OK
                )

        response = sorted(response, key=lambda value: value[1], reverse=True)[:5]

        return Response(
            list(map(
                lambda value: value[0],
                response
            )),
            status.HTTP_200_OK
        )


class FilterCitiesView(APIView):
    def get(self, request: Request):
        region = request.query_params.get("region")
        search = request.query_params.get("search")

        print(region)

        response = []

        if not search:
            return Response(
                [],
                status.HTTP_200_OK
            )

        if region not in REGIONS:
            return Response(
                {
                    "detail": "Регион не найден"
                },
                status.HTTP_400_BAD_REQUEST
            )

        for city in CITIES.get(region):
            coincidence = fuzz.ratio(search.lower(), city.lower())
            response.append((city, coincidence))

            if coincidence == 100:
                return Response(
                    [city],
                    status.HTTP_200_OK
                )


        response = sorted(response, key=lambda value: value[1], reverse=True)[:5]

        return Response(
            list(map(
                lambda value: value[0],
                response
            )),
            status.HTTP_200_OK
        )
