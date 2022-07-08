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