from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"items", views.ItemsView)
router.register(r"upload", views.UploadImageView, base_name="Item")
router.register(r"licenses", views.LicenseView, base_name="License")

urlpatterns = [path("", include(router.urls))]

