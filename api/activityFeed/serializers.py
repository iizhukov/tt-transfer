from rest_framework import serializers

from .models import News, ImageModel, FileModel
from api.authentication.serializers import GetUserSerializer


class NewsSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField()
    author = GetUserSerializer()

    class Meta:
        model = News
        fields = "__all__"
        depth = 2


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = "__all__"


class NewsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = "__all__"
