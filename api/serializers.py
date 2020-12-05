from rest_framework import serializers
from .models import Item, License, Purchase
from django.contrib.auth.models import User
from .b64 import Base64ImageField


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
        fields = ("id", "name", "tags", "price", "license", "owner", "image")

    def get_tags(self, obj):
        return str(obj.tags).split(";")


class ItemUploadSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Item
        fields = ("name", "tags", "price", "license", "image")
        extra_kwargs = {
            "name": {"allow_null": True, "required": False},
            "tags": {"allow_null": True, "required": False},
            "price": {"allow_null": True, "required": False},
            "license": {"allow_null": True, "required": False},
            "image": {"allow_null": True, "required": False},
        }

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["owner"] = user
        license = Item(**validated_data)
        license.save()
        return license

    def update(self, instance, validated_data):
        user = self.context.get("request").user
        if user.pk == instance.owner.pk:
            instance.name = validated_data.get("name", instance.name)
            instance.tags = validated_data.get("tags", instance.tags)
            instance.price = validated_data.get("price", instance.price)
            instance.license = validated_data.get("license", instance.license)
            instance.image = validated_data.get("image", instance.image)
            instance.save()
            return instance
        else:
            return None


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ("id", "merchant", "item")
        depth = 2


class MakePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ("item",)
