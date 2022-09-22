from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from insta_django.exceptions import NotAllowedMimetypeException
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.conf import settings
from tags.models import Tag
from .models import Post
from io import BytesIO
from PIL import Image
import os


class PostSerializer(serializers.ModelSerializer):
    medias = serializers.ListField(
        child=serializers.FileField(
            max_length=100000, allow_empty_file=False, use_url=False
        )
    )
    tags = serializers.ListField(child=serializers.CharField(max_length=50))

    def validate_medias(self, medias):
        print("self medias", medias)
        ALLOWED_MIMETYPES = [
            "image/jpg",
            "image/jpeg",
            "image/png",
            "video/mkv",
            "video/mov",
            "video/avi",
            "video/mp4",
        ]
        for media in medias:
            filename = media.name
            path = default_storage.save(filename, ContentFile(media.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            mimetype = media.content_type
            if mimetype not in ALLOWED_MIMETYPES:
                raise NotAllowedMimetypeException()

            if mimetype[0:5] == "image":
                self.image_resize(tmp_file)
            if mimetype[0:5] == "video":
                self.clip_video(tmp_file)

    class Meta:
        model = Post
        fields = [
            "id",
            "description",
            "tags",
            "medias",
            "owner",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["owner", "created_at", "updated_at"]

    def create(self, validated_data: dict) -> Post:

        medias = validated_data.pop("medias")
        tags = validated_data.pop("tags")
        post = Post.objects.create(**validated_data)

        for tag in tags:
            post_tag = get_object_or_404(Tag, name=tag)
            post.tags.add(post_tag)

        # return post

    def update(self, instance: Post, validated_data: dict) -> Post:

        if validated_data.get("description") == instance.description:
            validated_data.pop("description")

        if validated_data.get("tags"):
            tags = validated_data.pop("tags")
            instance.tags.remove(*instance.tags.all())
            for tag in tags:
                tag_name = tag["name"]
                post_tag = get_object_or_404(Tag, name=tag_name)
                instance.tags.add(post_tag)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    @classmethod
    def image_resize(self, image):
        img_io = BytesIO()
        img = Image.open(image)

        print("IMAGE SIZE", img.size)

    @classmethod
    def get_thumbnail(self, media, mimetype):
        pass

    @classmethod
    def clip_video(self, video):
        media_vine = ffmpeg_extract_subclip(video, 0, 10)
        print("MEDIA_VINE", media_vine)
