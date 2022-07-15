from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import serializers
from django.forms.models import model_to_dict

from .models import User, ResetPasswordCode


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'name', 'surname', 'patronymic', 'role',
            'phone', 'passport', 'email', 'password', 'confirmed'
        )

    def save(self, **kwargs):
        if not User.objects.filter(email=self.data['email']).first():
            usr = User.objects.create_user(**self.data)
            self.data.update(model_to_dict(usr))
            return True
        return False


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'name', 'surname', 'patronymic', 'role',
            'phone', 'passport', 'email', 'confirmed'
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    class Meta:
        fields = "__all__"


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', )


class CodeCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()

    class Meta:
        fields = ('code', 'email')


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()
    password = serializers.CharField()

    class Meta:
        fields = ('email', 'code', 'password')
