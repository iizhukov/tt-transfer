from rest_framework import serializers

from .models import News


class NewsSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField()

    class Meta:
        model = News
        fields = "__all__"
