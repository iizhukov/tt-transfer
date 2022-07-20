from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes as perm
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os

from api.permissions import IsManagerOrAdminUser
from .models import News, ImageModel, FileModel
from api.authentication.models import User
from .serializers import (
    NewsSerializer, NewsImageSerializer, NewsFileSerializer,
)


class NewsView(APIView):
    # permission_classes = (AllowAny, )
    
    def get(self, request):
        # user = request.user
        user = User.objects.get(email="admin@adm.py")

        news = News.objects.filter(
            category__in=set((
                get_category_by_role(user.role),
                "all"
            ))
        ).order_by("-date")

        serializered_news = NewsSerializer(data=news, many=True)
        serializered_news.is_valid()

        return Response(serializered_news.data, status=status.HTTP_200_OK)

    def post(self, request):
        # user = request.user
        user = User.objects.get(email="admin@adm.py")

        if user.role not in ("a", "m"):
            return Response({ "detail": "Недостаточно прав" }, status=status.HTTP_400_BAD_REQUEST)

        serializered_news = NewsSerializer(data=request.data)

        if serializered_news.is_valid():
            serializered_news.save()
            return Response(serializered_news.data, status=status.HTTP_201_CREATED)
        
        return Response({ "detail": "Некорректные данные"}, status=status.HTTP_400_BAD_REQUEST)


class NewsImageView(APIView):
    serializer_class = NewsImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny, )

    def get(self, request):
        if "id" not in request.data:
            return Response({"detail": "Где id?"}, status=status.HTTP_400_BAD_REQUEST)
        
        id = request.data.get("id")
        news = News.objects.filter(id=id).first()

        if not news:
            return Response({"detail": "Нет такой новости"}, status=status.HTTP_400_BAD_REQUEST)

        path = settings.PROJECT_URL
        client_path = os.path.join(path, f"client\\public\\uploads\\news\\images\\{news.id}")

        dir = []

        if os.path.exists(client_path):
            dir = os.listdir(client_path)

            print(dir)

        return Response({"images": dir}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NewsImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({}, status=status.HTTP_200_OK)
        return Response({"detail": "Не ваалид :("}, status=status.HTTP_400_BAD_REQUEST)


class NewsFileView(APIView):
    serializer_class = NewsFileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsManagerOrAdminUser, )

    def get(self, request):
        if "id" not in request.data:
            return Response({"detail": "Где id?"}, status=status.HTTP_400_BAD_REQUEST)
        
        id = request.data.get("id")
        news = News.objects.filter(id=id).first()

        if not news:
            return Response({"detail": "Нет такой новости"}, status=status.HTTP_400_BAD_REQUEST)

        path = settings.PROJECT_URL
        client_path = os.path.join(path, f"client\\public\\uploads\\news\\files\\{news.id}")

        dir = []

        if os.path.exists(client_path):
            dir = os.listdir(client_path)

            print(dir)

        return Response({"files": dir}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NewsFileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({}, status=status.HTTP_200_OK)
        return Response({"detail": "Не ваалид :("}, status=status.HTTP_400_BAD_REQUEST)


def get_category_by_role(role) -> str:
    if role == "c":
        return "for_clients"
    
    if role == "d":
        return "for_drivers"
    
    if role == "m":
        return "for_managers"
    
    return "all"
