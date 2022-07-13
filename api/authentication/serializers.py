from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import serializers
from django.forms.models import model_to_dict

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'name', 'surname', 'patronymic', 'role',
            'phone', 'passport', 'email', 'password'
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
            'phone', 'passport', 'email',
        )


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
