from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.forms import model_to_dict

from api.permissions import IsManagerOrAdminUser
from api.profile.models import Driver
from api.authentication.models import UserDocument
from api.cars.serializers import CarWithOutUserSerializer
from api.cars.models import Car
from api.profile.serializers import DriverSerializer, DocumentSerializer, ProtectedGetUserSerializer



class DriverView(APIView):
    serializer_class = DriverSerializer
    permission_classes = (IsManagerOrAdminUser, )

    def get(self, request, id=None):
        if id:
            return self.get_by_id(request, id)
        else:
            return self.get_list(request)

    def get_list(self, request):
        serializer = self.serializer_class(
            Driver.objects.all(),
            many=True
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def get_by_id(self, request, id):
        driver = get_object_or_404(
            Driver,
            id=id
        )

        serializer = self.serializer_class(
            driver
        )

        serializer.data["user"]["documents"] = [
            doc['document'] for doc in DocumentSerializer(
                UserDocument.objects.filter(user=driver.user),
                many=True
            ).data
        ]

        response = {
            **serializer.data,
            "cars": CarWithOutUserSerializer(
                Car.objects.filter(
                    user=driver.user
                ),
                many=True
            ).data
        }

        return Response(
            response,
            status.HTTP_200_OK
        )
    
    # def post(self, request):
    #     serializer = self.serializer_class(
    #         data={
    #             **request.data
    #         }
    #     )
