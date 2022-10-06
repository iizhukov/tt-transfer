from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import serializers
from django.forms.models import model_to_dict

from api.authentication.models import User, UserDocument
from api.cars.serializers import CarSerializer, CarWithOutUserSerializer
from api.authentication.serializers import ProtectedGetUserSerializer
from api.profile.models import Company, Manager, Client, Driver, Admin, EmployeeModel


class ChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField()
    newPassword = serializers.CharField()

    class Meta:
        fields = "__all__"


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'surname', "name", "patronymic")


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('avatar',)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = ('document',)


class EmployeeSerializer(serializers.ModelSerializer):
    user = ProtectedGetUserSerializer(read_only=True)

    class Meta:
        model = EmployeeModel
        fields = "__all__"
        depth = 1


class CompanySerializer(serializers.ModelSerializer):
    owner = ProtectedGetUserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = "__all__"
        depth = 2


class ManagerSerializer(serializers.ModelSerializer):
    user = ProtectedGetUserSerializer()

    class Meta:
        model = Manager
        fields = "__all__"
        depth = 1


class ClientSerializer(serializers.ModelSerializer):
    user = ProtectedGetUserSerializer()

    class Meta:
        model = Client
        fields = "__all__"
        depth = 1


class DriverSerializer(serializers.ModelSerializer):
    user = ProtectedGetUserSerializer()
    cars = CarWithOutUserSerializer(allow_null=True, many=True)

    class Meta:
        model = Driver
        fields = "__all__"
        depth = 2


class AdminSerializer(serializers.ModelSerializer):
    user = ProtectedGetUserSerializer()

    class Meta:
        model = Admin
        fields = "__all__"
        depth = 1
