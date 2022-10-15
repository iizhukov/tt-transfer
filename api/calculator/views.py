from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .controllers import URLMapController, CostCalculationController
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
