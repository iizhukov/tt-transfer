from rest_framework import serializers

from .models import News, ImageModel, FileModel


class NewsSerializer(serializers.ModelSerializer):
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
