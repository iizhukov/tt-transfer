from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.forms.models import model_to_dict
from django.utils import timezone
from django.conf import settings
from random import randint
import os

from .models import User, ResetPasswordCode
from .email import SendCode
from .serializers import (
    UserSerializer, GetUserSerializer,
    CookieTokenRefreshSerializer, ChangePasswordSerializer,
    UserEmailSerializer, CodeCodeSerializer, ResetPasswordSerializer,
    UserEditSerializer, AvatarSerializer
)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        user_sample = {
            "email": "",
            "password": "",
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
                return Response(serializered_user.data, status=status.HTTP_200_OK)

            return Response(
                {"detail": "Пользователь с такой почтой уже существует"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"detail": "Некорректные данные"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.data = {"detail": "Пользователь вышел из аккаунта"}

        response.delete_cookie("refresh_token")

        if request.COOKIES.get('refresh_token'):
            del request.COOKIES['refresh_token']

        return response


class ResetPasswordGetCodeView(APIView):
    serializer_class = UserEmailSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        if "email" in request.data:
            email = request.data.get("email")
            user = User.objects.filter(email=email).first()

            if user:
                code = ResetPasswordCode(user=user)
                code.code = randint(111111, 999999)
                code.end_datetime = timezone.now() + timezone.timedelta(minutes=5)
                code.save()
                print(code)

                # mail = SendCode((email, ))
                # mail.send_code(code.code)

                return Response({"detail": "Письмо отправлено с кодом отправлено"}, status=status.HTTP_200_OK)

            return Response({"detail": "Почта не идентифицирована"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Неверный запрос"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordCheckCodeView(APIView):
    serializer_class = CodeCodeSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        if "code" in request.data:
            sent_code = request.data.get("code")
            sent_email = request.data.get("email")
            code = ResetPasswordCode.objects.filter(code=sent_code).first()

            if not code or sent_email != code.user.email:
                return Response({"detail": "Не правильный код"}, status=status.HTTP_400_BAD_REQUEST)

            if code.end_datetime < timezone.now():
                code.delete()
                return Response({"detail": "Время действия кода истекло"}, status=status.HTTP_403_FORBIDDEN)

            return Response({"detail": "Соответствующий код"}, status=status.HTTP_200_OK)
        return Response({"detail": "Неверный запрос"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            code = ResetPasswordCode.objects.filter(
                code=serializer.data.get("code")
            ).first()

            email = serializer.data.get("email")
            user = User.objects.get(email=email)

            if not code:
                return Response({"detail": "Не правильный код"}, status=status.HTTP_400_BAD_REQUEST)

            if user.email != email and user != code.user:
                return Response({"detail": "Не правильный email"}, status=status.HTTP_400_BAD_REQUEST)

            new_password = serializer.data.get("password")
            user.set_password(new_password)
            user.save()

            code.delete()

            return Response({"detail": "Пароль сменен"}, status=status.HTTP_200_OK)
        return Response({"detail": "Неверный запрос"}, status=status.HTTP_400_BAD_REQUEST)


class GetUserDataView(APIView):
    def get(self, request):
        user = model_to_dict(request.user)
        serializered_user = GetUserSerializer(data=user)
        serializered_user.is_valid()
        return Response(data=serializered_user.data, status=status.HTTP_200_OK)


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
    permission_classes = (AllowAny, )

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
    permission_classes = (AllowAny, )

    def post(self, request, format=None):
        user = request.user
        user = User.objects.get(email="admin@adm.py")

        serializer = AvatarSerializer(instance=user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            
            return Response({"avatar": user.avatar.url}, status=status.HTTP_200_OK)
        return Response({"avatar": None}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        user = User.objects.get(email="admin@adm.py")

        avatar = user.avatar.url if user.is_authenticated and user.avatar else None

        return Response(data={"avatar": avatar}, status=status.HTTP_404_NOT_FOUND)


class IsAuthView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"status": True}, status=status.HTTP_200_OK)
        return Response({"status": False}, status=status.HTTP_401_UNAUTHORIZED)


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=response.data["refresh"],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            # del response.data['refresh']

        if response.data.get("access"):
            access = AccessToken(response.data["access"])
            user = User.objects.filter(id=access["user_id"]).first()

            if user:
                print(model_to_dict(user))
                serialized_user = GetUserSerializer(data=model_to_dict(user))
                serialized_user.initial_data["avatar"] = user.get_avatar_name()
                serialized_user.is_valid()

                response.data["user"] = serialized_user.data

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer
    permission_classes = (AllowAny, )

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=response.data["refresh"],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            # del response.data["refresh"]

        if response.data.get("access"):
            access = AccessToken(response.data["access"])
            user = User.objects.filter(id=access["user_id"]).first()

            if user:
                serialized_user = GetUserSerializer(data=model_to_dict(user))
                serialized_user.initial_data["avatar"] = user.get_avatar_name()
                serialized_user.is_valid()

                response.data["user"] = serialized_user.data

        return super().finalize_response(request, response, *args, **kwargs)


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


# class TokenObtainPairView(APIView):
#     permission_classes = (AllowAny, )
#     serializer_class = UserLoginSerializer

#     def post(self, request):
#         user_serializer = UserLoginSerializer(data=request.data)
#         user_serializer.is_valid()

#         user = authenticate(
#             email=user_serializer.data.get("email"),
#             password=user_serializer.data.get("password")
#         )

#         response = Response(status=status.HTTP_200_OK)

#         if user is not None:
#             if user.is_active:
#                 data = get_tokens_for_user(user)
#                 csrf.get_token(request)

#                 response.set_cookie(
#                     key=settings.SIMPLE_JWT["AUTH_COOKIE"],
#                     value=data["refresh"],
#                     expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
#                     secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
#                     httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
#                     samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
#                 )

#                 response.data = {
#                     "access_token": data["access"]
#                 }

#                 return response
#             else:
#                 return Response({ "detail" : "Аккаунт не активен" }, status=status.HTTP_404_NOT_FOUND)

#         return Response({ "detail" : "Неверная почта или пароль" }, status=status.HTTP_404_NOT_FOUND)


# class TokenRefreshView(APIView):
#     def get(self, request):
#         refresh_token = request.COOKIES.get('refresh_token')

#         return Response(data={}, status=status.HTTP_200_OK)
