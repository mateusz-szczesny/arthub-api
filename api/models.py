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

    def __str__(self):
        return f"Name: {self.name} | Abbreviation: {self.content} | Owner: {self.owner.username}"


class Item(models.Model):
    name = models.CharField(max_length=128)
    tags = models.CharField(max_length=2048)
    license = models.ForeignKey(
        License, on_delete=models.DO_NOTHING, related_name="items", null=True
    )
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="items")
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def image_base64(self):
        return image_as_base64(self.image.path)

    def __str__(self):
        return f"Name: {self.name} | Tags: {self.tags} | Price: {self.price} | Owner: {self.owner.username}"

class Purchase(models.Model):
    merchant = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="purchases")
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, related_name="purchases")

    def __str__(self):
        return f"Merchant: {self.merchant.username} | Item: {self.item.name}"