from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import News
from .serializers import NewsSerializer


class NewsListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        news = News.objects.all()
        serializered_news = NewsSerializer(data=news, many=True)
        serializered_news.is_valid()
        return Response(serializered_news.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializered_new = NewsSerializer(data=request.data)

        if serializered_new.is_valid():
            serializered_new.save()
            return Response(serializered_new, status=status.HTTP_201_CREATED)
        
        return Response(data={ "detail": "Некорректные данные"}, status=status.HTTP_400_BAD_REQUEST)
