from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework.generics import ListAPIView
from django.forms.models import model_to_dict
from django.contrib.auth import login, authenticate
from django.middleware import csrf
from django.http import HttpResponseRedirect

from tt_transfer import settings
from .models import User
from .serializers import (
    UserSerializer, UserLoginSerializer, GetUserSerializer,
    CookieTokenRefreshSerializer, ChangePasswordSerializer,
)

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


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
                # return HttpResponseRedirect(
                #     reverse("token_obtain_pair")
                # )

            return Response(
                { "detail": "Пользователь с такой почтой уже существует" },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response({ "detail": "Некорректные данные"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def post(self, request):
        print(request.user)

        serialized_password = ChangePasswordSerializer(data=request.data)
        
        if serialized_password.is_valid():
            if serialized_password.data.get("new_password1") == serialized_password.data.get("new_password2"):
                password = serialized_password.data.get("new_password1")

                request.user.set_password(password)
                request.user.save()
    
                return Response(data={ "detail": "Пароль успешно изменен" }, status=status.HTTP_200_OK)
            
            return Response(data={ "detail": "Пароли не совпадают" }, status=status.HTTP_400_BAD_REQUEST)

        return Response(data={ "detail": "Данные не валидны" }, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 15
        response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)

        access = AccessToken(response.data["access"])
        user = User.objects.get(id=access["user_id"])

        serialized_user = GetUserSerializer(data=model_to_dict(user))
        serialized_user.is_valid()

        response.data["user"] = serialized_user.data
        del response.data['refresh']

    return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 15
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True, samesite="Strict")
    
            del response.data['refresh']
    
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
