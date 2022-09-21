from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "password",
            "email",
            "private_profile",
        ]

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)
        
        return user

    def update(self, instance: User, validated_data: dict) -> User:

        if validated_data.get("password"):
            password = validated_data.pop("password")

        if validated_data.get("email") == instance.email:
            validated_data.pop("email")

        if validated_data.get("name") == instance.name:
            validated_data.pop("name")

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance
