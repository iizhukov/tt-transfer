from urllib.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import CarSerializer
from api.permissions import IsDriverUser, IsManagerUser
from api.authentication.models import User
from api.authentication.serializers import GetUserSerializer
from .models import Car, CAR_CLASSES


class CarsListView(APIView):
    permission_classes = (IsAuthenticated, IsManagerUser, IsAdminUser)

    def get(self, request):
        pass


class UserCarView(APIView):
    permission_classes = (IsAuthenticated, IsDriverUser, )

    def get(self, request) -> Response:
        try:
            user_car = Car.objects.get(owner=request.user)
            user = GetUserSerializer(
                data=User.objects.get(pk=request.user.id).__dict__
            )
            user.is_valid()

            serializered_car = CarSerializer(
                data={
                    **user_car.__dict__,
                    "owner": user.data,
                }
            )
            serializered_car.is_valid()

            return Response(
                serializered_car.data,
                status=status.HTTP_200_OK
            )
        except Car.DoesNotExist:
            return Response(
                data={ "detail": "Автомобиль не найден" },
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        pass


class GetCarClassesView(APIView):
    def get(self, request: Request):
        response = []

        for car_class in CAR_CLASSES:
            response.append({
                "title": car_class[1],
                "slug": car_class[0]
            })

        return Response(
            response,
            status.HTTP_200_OK
        )
