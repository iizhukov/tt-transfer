from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.forms.models import model_to_dict

from api.authentication.models import User, UserDocument
from api.authentication.serializers import (
    GetUserSerializer, UserSerializer
)
from .serializers import (
    ChangePasswordSerializer, UserEditSerializer,
    AvatarSerializer, DocumentSerializer,
    CompanySerializer
)


class ChangePasswordView(APIView):
    def post(self, request):
        serialized_password = ChangePasswordSerializer(data=request.data)

        if serialized_password.is_valid():
            old_password = serialized_password.data.get("oldPassword")
            new_password = serialized_password.data.get("newPassword")

            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()

                return Response(data={"detail": "Пароль успешно изменен"}, status=status.HTTP_200_OK)
            return Response({"detail": "Старый пароль не подходит"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"detail": "Данные не валидны"}, status=status.HTTP_400_BAD_REQUEST)


class EditUserView(APIView):
    serializer_class = UserEditSerializer
    # permission_classes = (AllowAny, )

    def post(self, request):
        sample = {
            "phone": "",
            "surname": "",
            "name": "",
            "patronymic": "",
        }
        sample.update(request.data)
        serializer = UserEditSerializer(data=sample)

        if serializer.is_valid():
            user = request.user

            user.phone = serializer.data.get("phone") or user.phone
            user.surname = serializer.data.get("surname") or user.surname
            user.name = serializer.data.get("name") or user.name
            user.patronymic = serializer.data.get("patronymic") or user.patronymic

            request.user.save()
            return Response({"detail": "Данные изменены"}, status=status.HTTP_200_OK)
        return Response({"detail": "Некорректные данные"}, status=status.HTTP_400_BAD_REQUEST)


class UserAvatarView(APIView):
    serializer_class = AvatarSerializer
    parser_classes = (MultiPartParser, FormParser)
    # permission_classes = (AllowAny, )

    def post(self, request, format=None):
        user = request.user
        # user = User.objects.get(email="admin@adm.py")

        serializer = AvatarSerializer(instance=user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=request.user.email)
            avatar = user.avatar.url
            print(avatar)

            return Response({"avatar": avatar}, status=status.HTTP_200_OK)
        return Response({"avatar": user.avatar.url}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        # user = User.objects.get(email="admin@adm.py")

        avatar = user.avatar.url if user.is_authenticated and user.avatar else None

        return Response(data={"avatar": avatar}, status=status.HTTP_404_NOT_FOUND)


class UserDocumentsView(APIView):
    serializer_class = DocumentSerializer
    parser_classes = (MultiPartParser, FormParser)
    # permission_classes = (AllowAny, )

    def get(self, request):
        docs = UserDocument.objects.filter(user=request.user)
        # docs = UserDocument.objects.filter(user=User.objects.get(email="zxc@zxc.zxc"))
        return Response({"documents": [doc.document.url for doc in docs] }, status=status.HTTP_200_OK)

    def post(self, request):
        for file in request.data:
            doc = UserDocument(user=request.user)
            serializer = DocumentSerializer(instance=doc, data={"document": request.data.get(file)})

            if serializer.is_valid():
                serializer.save()

        documents = []

        for doc in UserDocument.objects.filter(user=request.user):
            documents.append(doc.document.url)
            
        return Response({"documents": documents}, status=status.HTTP_200_OK)


class GetUserDataView(APIView):
    def get(self, request):
        user = model_to_dict(request.user)
        serializered_user = GetUserSerializer(data=user)
        serializered_user.is_valid()
        return Response(data=serializered_user.data, status=status.HTTP_200_OK)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ContractorView(APIView):
    serializer_class = CompanySerializer
    # permission_classes = (AllowAny, )

    def get(self, request):
        user = request.user
    
        if not getattr(user, "company", False):
            return Response(
                {},
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = self.serializer_class(
            data=model_to_dict(user.company)
        )
        serializer.is_valid()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "detail": "Невалидные данные",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
