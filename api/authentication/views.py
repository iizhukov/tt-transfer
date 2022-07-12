from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from .models import User
from .serializers import UserSerializer


class CreateUserView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request):
        users = UserSerializer(data=User.objects.all(), many=True)
        users.is_valid()
        return Response(users.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_sample = {
            "name": "",
            "surname": "",
            "patronymic": "",
            "phone": "",
            "passport": "",
            "role": "c",
        }
        user_sample.update(request.data)
        serializered_user = UserSerializer(data=user_sample)

        if serializered_user.is_valid():
            if serializered_user.save():
                return Response(serializered_user.data, status=status.HTTP_201_CREATED)

            return Response(
                { "detail": "Пользователь с такой почтой уже существует" },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({ "detail": "Некорректные данные"}, status=status.HTTP_400_BAD_REQUEST)
