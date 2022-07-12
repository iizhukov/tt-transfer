from rest_framework import serializers
from django.forms.models import model_to_dict

from .models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'   
        # depth = 0