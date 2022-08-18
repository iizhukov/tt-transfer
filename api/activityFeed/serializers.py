from rest_framework import serializers

from .models import News, ImageModel, FileModel
from api.authentication.serializers import ProtectedGetUserSerializer


class NewsSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField()
    author = ProtectedGetUserSerializer()

    class Meta:
        model = News
        fields = "__all__"
        depth = 2


class CreateNewsSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField()

    class Meta:
        model = News
        fields = "__all__"


class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = "__all__"


class NewsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = "__all__"
