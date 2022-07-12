from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import News
from .serializers import NewsSerializer


class NewsView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        news = News.objects.order_by('-date')

        serializered_news = NewsSerializer(data=news, many=True)
        serializered_news.is_valid()

        return Response(serializered_news.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role not in ("a", "m"):
            return Response({ "detail": "Недостаточно прав" }, status=status.HTTP_400_BAD_REQUEST)

        serializered_news = NewsSerializer(data=request.data)

        if serializered_news.is_valid():
            serializered_news.save()
            return Response(serializered_news, status=status.HTTP_201_CREATED)
        
        return Response({ "detail": "Некорректные данные"}, status=status.HTTP_400_BAD_REQUEST)

