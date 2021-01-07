from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"items", views.ItemsView)
router.register(r"upload", views.UploadImageView, basename="Item")
router.register(r"licenses", views.LicenseView, basename="License")
router.register(r"purchase", views.PurchaseView, basename="Purchase")

urlpatterns = [
    path("", include(router.urls)),
    path("buy/", views.BuyView.as_view(), name="Buy"),
]

