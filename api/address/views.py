from django.forms import model_to_dict
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Address, City, CityZone, Coordinate
from .serializers import (
    CitySerializer, AddressSerializer,
    AddAddressSerializer, CityZoneSerializer,
)


class CityView(APIView):
    serializer_class = CitySerializer

    def get(self, request):
        serializer = self.serializer_class(
            data=City.objects.all(),
            many=True,
        )
        serializer.is_valid()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                {"detail": "Данные невалидны"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class AddressView(APIView):
    serializer_class = AddressSerializer

    def get(self, request):
        serializer = self.serializer_class(
            data=Address.objects.all(),
            many=True,
        )
        serializer.is_valid()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class AddAddressView(APIView):
    serializer_class = AddAddressSerializer

    def post(self, request):
        if not self.serializer_class(data=request.data).is_valid():
            return Response(
                {"detail": "Некорректные данные"},
                status.HTTP_400_BAD_REQUEST
            )
        
        city_serializer = CitySerializer(data=request.data)
        city_serializer.is_valid()

        if not City.objects.filter(
            city=city_serializer.validated_data.get('city')
        ).first():
            city_serializer.save()

        city = City.objects.filter(
            city=request.data.get('city')
        ).first()

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
    
    def get(self, request):
        serializer = self.serializer_class(
            data=CityZone.objects.filter(
                city=City.objects.filter(
                    region=request.data.get("region"),
                    city=request.data.get("city")
                ).first()
            ),
            many=True
        )
        serializer.is_valid()

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def post(self, request):
        city = City.objects.filter(
            region=request.data.get("region"),
            city=request.data.get("city")
        ).first()

        if not city:
            city = City(
                region=request.data.get("region"),
                city=request.data.get("city")
            )
            city.save()

        zone = CityZone(
            city=city,
            color=request.data.get("color")
        )
        zone.save()

        lst = request.data.get("coordinates")

        for latitude, longitude in lst:
            print(latitude, longitude)
            coords, created = Coordinate.objects.get_or_create(
                latitude=latitude,
                longitude=longitude
            )

            if created:
                coords.save()

            zone.coordinates.add(coords)


        serializer = CityZoneSerializer(
            instance=CityZone.objects.get(
                city=city,
                color=request.data.get("color")
            )
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )


class EditZoneView(APIView):
    serializer_class = CityZoneSerializer

    def get(self, reqeust, id: int):
        zone = CityZone.objects.filter(id=id).first()

        if not zone:
            return Response(
                {"detail": "Not Found"},
                status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(
            instance=zone
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def put(self, request, id):
        zone = CityZone.objects.filter(
            pk=id
        ).first()

        if not zone:
            return Response(
                {"detail": "Такой зоны нет"},
                status.HTTP_400_BAD_REQUEST
            )

        if CityZone.objects.filter(
            city=zone.city,
            color=request.data.get("new_color")
        ).first():
            return Response(
                {"detail": "Зона с таким цветом уже существует"},
                status.HTTP_400_BAD_REQUEST
            )

        new_color = request.data.get("new_color")
        new_coords = request.data.get("new_coordinates")

        if new_color:
            zone.color = new_color
        
        if new_coords:
            zone.coordinates.clear()

            for latitude, longitude in new_coords:
                print(latitude, longitude)
                coords, created = Coordinate.objects.get_or_create(
                    latitude=latitude,
                    longitude=longitude
                )

                if created:
                    coords.save()

                zone.coordinates.add(coords)

        zone.save()

        serializer = self.serializer_class(
            instance=zone
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def delete(self, request, id: int):
        zone = CityZone.objects.filter(id=id).first()

        if not zone:
            return Response(
                {"detail": "Not Found"},
                status.HTTP_400_BAD_REQUEST
            )

        zone.delete()

        return Response(
            {"detail": "deleted"},
            status.HTTP_200_OK
        )
