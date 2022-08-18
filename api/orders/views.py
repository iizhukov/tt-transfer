from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import (
    OrderSerializer, 
)
from .models import Order


class OrderView(APIView):
    serilizer_class = OrderSerializer

    def get(self, request):
        if request.user.role != "c":
            return Response(
                {"detail": "Вы не клиент"},
                status.HTTP_200_OK
            )

        serializer = self.serilizer_class(
            Order.objects.filter(
                contractor=request.user.company
            ),
            many=True
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def post(self, request):
        pass
    