from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .controllers import (
    URLMapController, CostCalculationController,
    LocationSearchController
)
from .route import Route, Point
from api.permissions import IsManagerOrAdminUser
from api.address.models import City, Hub, Coordinate


class TestView(APIView):
    controller = URLMapController

    def get(self, request: Request):
        # controller = CostCalculationController.intercity__hub__basic(
        #     City.objects.get(city="Москва"),
        #     Hub.objects.get(title="Оренбург Вокзал"),
        #     "standart"
        # )
        # controller.is_valid(raise_exception=True)
        
        # hub: Hub = Hub.objects.get(title="Оренбург Вокзал")
        coords1 = Coordinate(latitude=55.755819, longitude=37.617644)
        coords2 = Coordinate(latitude=51.802146, longitude=55.155175)
        
        
        controller = CostCalculationController.intracity__coords__basic(
            City.objects.get(city="Оренбург"),
            coords1,
            coords2,
            "standart"
        )
        controller.is_valid(raise_exception=True)

        return Response(
            controller.data,
            status.HTTP_200_OK
        )


class CalculatorView(APIView):
    def get(self, request: Request):
        points = request.query_params.getlist("points")
        car_class = request.query_params.get("car_class")

        if len(points) < 2:
            return Response(
                {
                    "detail": "Введите минимум два адреса"
                },
                status.HTTP_400_BAD_REQUEST
            )

        points = [
            LocationSearchController.parse_point(point)
            for point in points
        ]
        
        controller = CostCalculationController.count_price(points, car_class)
        
        return Response(
            controller.data,
            status.HTTP_200_OK
        )


class CalculatorSearchView(APIView):
    def get(self, request: Request):
        search = request.query_params.get("search")
        limit = int(request.query_params.get("limit", 5))
        
        response_data = LocationSearchController.search(search)
        
        if len(response_data) < limit:
            response_data.extend(LocationSearchController.address_search(
                search,
                limit - len(response_data)
            ))
        
        return Response(
            response_data[:limit],
            status.HTTP_200_OK
        )
