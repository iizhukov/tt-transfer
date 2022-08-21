from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.forms import model_to_dict
from django.conf import settings

from api.permissions import IsManagerOrAdminUser
from .models import News, ImageModel, FileModel
from .serializers import (
    NewsSerializer, NewsImageSerializer, NewsFileSerializer,
    CreateNewsSerializer
)


class ResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class NewsView(APIView, ResultsSetPagination):  
    serializer_class = NewsSerializer

    def get(self, request):
        news = News.objects.filter(
            category__in=set((
                get_category_by_role(request.user.role),
                "for_all"
            ))
        ).order_by("-date")

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

        results = self.paginate_queryset(data, request, view=self)
        print(results)
        return self.get_paginated_response(results)

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role not in ("a", "m"):
            return Response({ "detail": "Недостаточно прав" }, status=status.HTTP_400_BAD_REQUEST)

        serializered_news = CreateNewsSerializer(
            data={
                **request.data,
                "author": request.data.get("author") or request.user.id,
            }
        )

        if serializered_news.is_valid():
            serializered_news.save()
            return Response(serializered_news.data, status=status.HTTP_201_CREATED)
        
        return Response(
            serializered_news.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class NewsImageView(APIView):
    serializer_class = NewsImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id):
        news = get_object_or_404(
            News,
            id=id
        )

        return Response(
            {"images": NewsImageView._get_image_by_news(news=news)},
            status=status.HTTP_200_OK
        )

    def post(self, request, id):
        news = get_object_or_404(
            News,
            id=id
        )

        for image in request.FILES.getlist("images"):
            news_image = ImageModel(news=news)
            serializer = NewsImageSerializer(
                instance=news_image,
                data={
                    "image": image
                }
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

    def get(self, request, id):
        news = get_object_or_404(
            News,
            id=id
        )

        return Response(
            {"files": NewsFileView._get_files_by_news(news=news)},
            status=status.HTTP_200_OK
        )

    def post(self, request, id):
        news = get_object_or_404(
            News,
            id=id
        )

        for file in request.FILES.getlist("files"):
            news_file = FileModel(news=news)

            serializer = NewsFileSerializer(
                instance=news_file,
                data={
                    "file": file
                }
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
