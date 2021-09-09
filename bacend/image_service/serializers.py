from rest_framework import serializers
from .models import Image
from rest_framework.serializers import ModelSerializer


class ImageSerializer(ModelSerializer):
    """This serializer for image-model"""
    class Meta:
        model = Image
        fields = "__all__"
