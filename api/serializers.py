from rest_framework import serializers
from .models import Item, License
from django.contrib.auth.models import User


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ("id", "name", "content", "default")
        extra_kwargs = {"id": {"read_only": True}, "default": {"read_only": True}}

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["owner"] = user
        validated_data["default"] = False
        license = License(**validated_data)
        license.save()
        return license

    def update(self, instance, validated_data):
        user = self.context.get("request").user
        if user.pk == instance.owner.id:
            instance.name = validated_data.get("name", instance.name)
            instance.content = validated_data.get("content", instance.content)
            instance.save()
            return instance
        else:
            return None


class ItemSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    owner = OwnerSerializer()

    class Meta:
        model = Item
        depth = 1
        fields = ("id", "name", "tags", "owner", "image")

    def get_tags(self, obj):
        return str(obj.tags).split(";")

