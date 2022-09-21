from wsgiref import validate
from tags.serializers import TagNameSerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from tags.models import Tag
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    tags = TagNameSerializer(many=True)

    class Meta:
        model = Post
        fields = ["id", "description", "tags", "owner", "created_at", "updated_at"]
        read_only_fields = ["owner", "created_at", "updated_at"]
        # depth = 1

    def create(self, validated_data: dict) -> Post:
        tags = validated_data.pop("tags")
        post = Post.objects.create(**validated_data)
        for tag in tags:
            tag_name = tag["name"]
            post_tag = get_object_or_404(Tag, name=tag_name)
            post.tags.add(post_tag)

        return post

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
