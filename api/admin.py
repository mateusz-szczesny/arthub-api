from django.contrib import admin
from .models import Item, License, Purchase

admin.site.register(Item)
admin.site.register(License)
admin.site.register(Purchase)
