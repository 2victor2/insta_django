from rest_framework import serializers
from .models import PostMedia


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ["id", "mimetype", "thumbnail", "media"]
        read_only_fields = ["mimetype", "thumbnail"]
