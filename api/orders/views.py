from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import (
    OrderSerializer, 
)


class OrderView(APIView):
    serilizer_class = OrderSerializer
    permission_classes = (AllowAny, )

    def get(self, request):
        serializer = self.serilizer_class()
        return Response()

    def post(self, request):
        pass
