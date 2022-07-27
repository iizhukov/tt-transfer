from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import serializers
from django.forms.models import model_to_dict

from api.authentication.models import User, UserDocument
from api.profile.models import Company


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
        fields = ('avatar', )


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = ('document', )


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
