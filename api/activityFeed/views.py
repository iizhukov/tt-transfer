from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import News
from .serializers import NewsSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def get_news(request, number=None):
    if request.method == "GET":
        if number:
            news = News.objects.order_by("-creation_date")[:number]
        else:
            news = News.objects.order_by("-creation_date")

        serializered_news = NewsSerializer(data=news, many=True)
        serializered_news.is_valid()
        return Response(
            serializered_news.data,
            status=status.HTTP_200_OK,
        )
    elif request.method == "POST":
        serializer = NewsSerializer(data=request.data)
        serializer.initial_data["author"] = request.user.id

        if serializer.is_valid():
            serializer.save()
    
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
