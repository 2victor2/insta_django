from utils.file_management import get_thumbnail, resize_image, subclip_video
from post_medias.serializers import PostMediaSerializer
from django.core.files.storage import default_storage
from tags.serializers import TagNameSerializer
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from post_medias.models import PostMedia
from insta_django.exceptions import (
    NotAllowedMimetypeException,
    NotAllowedMoreThan10TagsException,
)
from rest_framework import serializers
from django.conf import settings
from tags.models import Tag
from .models import Post
import os


class PostSerializer(serializers.ModelSerializer):
    medias = PostMediaSerializer(many=True, read_only=True)
    tags = TagNameSerializer(many=True, read_only=True)
    post_medias = serializers.ListField(
        child=serializers.FileField(
            max_length=100000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
    )
    post_tags = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True
    )

    def validate_post_tags(self, tags):
        if len(tags) > 10:
            raise NotAllowedMoreThan10TagsException()

        return tags

    def validate_post_medias(self, medias):
        validated_medias = []
        ALLOWED_MIMETYPES = [
            "image/jpg",
            "image/jpeg",
            "image/png",
            # "video/mkv",
            # "video/mov",
            # "video/avi",
            # "video/mp4",
        ]

        for media in medias:
            filename = media.name
            path = default_storage.save(filename, ContentFile(media.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            if media.content_type not in ALLOWED_MIMETYPES:
                raise NotAllowedMimetypeException()

            if media.content_type[0:5] == "image":
                image_content, mimetype = resize_image(tmp_file)

                image_thumb = get_thumbnail(tmp_file)
                validated_medias.append(
                    {
                        "raw_content": image_content,
                        "raw_thumbnail": image_thumb,
                        "mimetype": mimetype,
                    }
                )

            # if media.content_type[0:5] == "video":
            #     video_content, video_thumb, mimetype = subclip_video(tmp_file)

            #     validated_medias.append(
            #         {
            #             "raw_content": video_content,
            #             "raw_thumbnail": video_thumb,
            #             "mimetype": mimetype,
            #         }
            #     )

            os.remove(tmp_file)

        return validated_medias

    class Meta:
        model = Post
        fields = [
            "id",
            "description",
            "post_tags",
            "post_medias",
            "tags",
            "medias",
            "owner",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "owner",
            "created_at",
            "updated_at",
            "tags",
            "medias",
        ]

    def create(self, validated_data: dict) -> Post:

        medias = validated_data.pop("post_medias")
        tags = validated_data.pop("post_tags")
        post = Post.objects.create(**validated_data)
        for media in medias:
            content, thumb, mimetype = media.values()
            PostMedia.objects.create(
                mimetype=mimetype, thumbnail=thumb, media=content, post=post
            )

        for tag in tags:
            post_tag = get_object_or_404(Tag, name=tag)
            post.tags.add(post_tag)

        return post

    def update(self, instance: Post, validated_data: dict) -> Post:

        if validated_data.get("description") == instance.description:
            validated_data.pop("description")

        if validated_data.get("post_tags"):
            tags = validated_data.pop("post_tags")
            instance.tags.remove(*instance.tags.all())
            for tag in tags:
                post_tag = get_object_or_404(Tag, name=tag)
                instance.tags.add(post_tag)

        if validated_data.get("post_medias"):
            medias = validated_data.pop("post_medias")
            PostMedia.objects.filter(post=instance).delete()
            for media in medias:
                content, thumb, mimetype = media.values()
                PostMedia.objects.create(
                    mimetype=mimetype, thumbnail=thumb, media=content, post=instance
                )

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
