from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TagNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Tag
        fields = ["name"]
