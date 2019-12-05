from django.db import models
from django.conf import settings
from .utils import image_as_base64
from django.utils.html import format_html
from django.contrib.auth.models import User


class License(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="licenses")
    content = models.CharField(max_length=4096)
    default = models.BooleanField(default=True)


class Item(models.Model):
    name = models.CharField(max_length=128)
    tags = models.CharField(max_length=2048)
    license = models.ForeignKey(
        License, on_delete=models.DO_NOTHING, related_name="items", null=True
    )
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="items")
    image = models.ImageField(upload_to="images/%Y/%m/%d")

    @property
    def image_base64(self):
        return image_as_base64(self.image.path)

