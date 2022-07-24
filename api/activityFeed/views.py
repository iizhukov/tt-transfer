from email.errors import NoBoundaryInMultipartDefect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes as perm
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.forms import model_to_dict
from django.conf import settings
import os

from api.permissions import IsManagerOrAdminUser
from .models import News, ImageModel, FileModel
from api.authentication.models import User
from .serializers import (
    NewsSerializer, NewsImageSerializer, NewsFileSerializer,
)


class NewsView(APIView):    
    def get(self, request, limit=None):
        user = request.user
        # user = User.objects.get(email="admin@adm.py")

        news = News.objects.filter(
            category__in=set((
                get_category_by_role(user.role),
                "for_all"
            ))
        ).order_by("-date")[:limit]

        serializered_news = NewsSerializer(data=news, many=True)
        serializered_news.is_valid()

        data = []
        for news_ in serializered_news.data:
            news_ = dict(news_)
            images = NewsImageView._get_image_by_news(news_["id"])
            files = NewsFileView._get_files_by_news(news_["id"])

            news_data = {
                **news_,
                "images": images,
                "files": files
            }
            data.append(news_data)

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        # user = User.objects.get(email="admin@adm.py")

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

    def get(self, request):
        if "id" not in request.data:
            return Response({"detail": "Где id?"}, status=status.HTTP_400_BAD_REQUEST)
        
        id = request.data.get("id")
        news = News.objects.filter(id=id).first()

        if not news:
            return Response({"detail": "Нет такой новости"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"images": NewsImageView._get_image_by_news(news=news)},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        news = News.objects.get(id=request.data.get("news"))

        for image in request.data:
            news_image = ImageModel(news=news)
            serializer = NewsImageSerializer(
                instance=news_image,
                data={"image": request.data.get(image)}
            )

            if serializer.is_valid():
                serializer.save()

        return Response(
            {"images": NewsImageView._get_image_by_news(news)},
            status=status.HTTP_200_OK
        )

    @staticmethod
    def _get_image_by_news(news):
        images = []

        for image in ImageModel.objects.filter(news=news):
            images.append(image.image.url)

        return images


class NewsFileView(APIView):
    serializer_class = NewsFileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        if "id" not in request.data:
            return Response({"detail": "Где id?"}, status=status.HTTP_400_BAD_REQUEST)
        
        id = request.data.get("id")
        news = News.objects.filter(id=id).first()

        if not news:
            return Response({"detail": "Нет такой новости"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"files": NewsFileView._get_files_by_news(news=news)},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        news = News.objects.get(id=request.data.get("news"))

        for file in request.data:
            news_file = FileModel(news=news)
            serializer = NewsImageSerializer(
                instance=news_file,
                data={"file": request.data.get(file)}
            )

            if serializer.is_valid():
                serializer.save()

        return Response(
            {"files": NewsFileView._get_files_by_news(news=news)},
            status=status.HTTP_200_OK
        )

    @staticmethod
    def _get_files_by_news(news):
        files = []

        for file in FileModel.objects.filter(news=news):
            files.append(file.file.url)

        return files


def get_category_by_role(role) -> str:
    if role == "c":
        return "for_clients"
    
    if role == "d":
        return "for_drivers"
    
    if role == "m":
        return "for_managers"
    
    return "for_all"
