from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import City
from .serializers import CitySerializer


class CityView(APIView):
    serializer_class = CitySerializer

    def get(self, request):
        pass

    def post(self, request):
        pass

