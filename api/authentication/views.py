from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.middleware import csrf
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from tt_transfer import settings
from .models import User
from .serializers import UserSerializer, UserLoginSerializer, CookieTokenRefreshSerializer


class CreateUserView(APIView):
    @permission_classes((IsAdminUser, ))
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


class CookieTokenObtainPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 15
        response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)

        del response.data['refresh']

    return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 15
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
    
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
