from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from validate_email import validate_email

from .models import Company, EmployeeModel
from api.authentication.models import User, UserDocument
from api.address.models import City, Address
from .email import SendEmployeePassword
from api.authentication.serializers import (
    GetUserSerializer, UserSerializer
)
from .serializers import (
    ChangePasswordSerializer, UserEditSerializer,
    AvatarSerializer, DocumentSerializer,
    CompanySerializer, EmployeeSerializer
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
        return Response({"documents": [doc.document.url for doc in docs]}, status=status.HTTP_200_OK)

    def post(self, request):
        for file in request.FILES.getlist("documents"):
            doc = UserDocument(user=request.user)
            serializer = DocumentSerializer(
                instance=doc,
                data={
                    "document": file
                }
            )

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


class CompanyEmployeeView(APIView):
    serializer_class = EmployeeSerializer

    def post(self, request: Request, company_id):
        # if not CompanyEmployeeView._check_email(request.data.get("email")):
        #     return Response(
        #         {
        #             "detail": "Некорректная почта"
        #         },
        #         status.HTTP_400_BAD_REQUEST
        #     )

        email = request.data.get("email")
        password = User.objects.generate_password()

        if User.objects.filter(email=email):
            return Response(
                {
                    "detail": "Пользователь с такой почтой уже существует"
                },
                status.HTTP_400_BAD_REQUEST
            )

        user_employee = User.objects.create_user(
            email,
            password,
            name=request.data.get("name"),
            surname=request.data.get("surname"),
            patronymic=request.data.get("patronymic"),
            phone=request.data.get("phone"),
            role="e"
        )

        employee = EmployeeModel.objects.create(
            user=user_employee
        )

        SendEmployeePassword((email,)).send_password(password)

        Company.objects.get(
            pk=company_id
        ).employees.add(employee)

        serializer = EmployeeSerializer(
            employee
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    @staticmethod
    def _check_email(email):
        return validate_email(email, verify=True)


class CompanyView(APIView):
    serializer_class = CompanySerializer

    def get(self, request, id: int = None):
        if id:
            serializer = self.serializer_class(
                get_object_or_404(
                    Company,
                    pk=id
                )
            )
        else:
            serializer = self.serializer_class(
                Company.objects.filter(
                    owner=request.user
                ),
                many=True
            )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data
        )

        city = get_object_or_404(
            City,
            region=request.data.get("region"),
            city=request.data.get("city")
        )

        address, _ = Address.objects.get_or_create(
            city=city,
            street=request.data.get("street"),
            number=request.data.get("number")
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(
            owner=request.user,
            address=address
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, id):
        company = get_object_or_404(
            Company,
            id=id,
            user=request.user
        )

        company.delete()

        return Response(
            {"detail": "deleted"},
            status.HTTP_200_OK
        )

    def put(self, request, id):
        company = get_object_or_404(
            Company,
            id=id
        )

        city = get_object_or_404(
            City,
            region=request.data.get("region"),
            city=request.data.get("city")
        )

        address, _ = Address.objects.get_or_create(
            city=city,
            street=request.data.get("street"),
            number=request.data.get("number")
        )

        serializer = self.serializer_class(
            company,
            request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST
            )

        serializer.save(
            address=address
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )
