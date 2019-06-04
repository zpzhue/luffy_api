from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from home import models

class BannerInfoSerializer(ModelSerializer):
    image = serializers.URLField(max_length=150)
    class Meta:
        model = models.BannerInfo
        fields = ['name', 'link', 'image']