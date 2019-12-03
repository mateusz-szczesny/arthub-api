from rest_framework import serializers
from .models import Item, License
from django.contrib.auth.models import User


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class ItemSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    owner = OwnerSerializer()

    class Meta:
        model = Item
        depth = 1
        fields = ("id", "name", "tags", "owner", "image")

    def get_tags(self, obj):
        return str(obj.tags).split(";")

