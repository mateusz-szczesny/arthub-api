from rest_framework import parsers, renderers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, mixins
from rest_framework.viewsets import GenericViewSet
from .models import Item, License, Purchase
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponseBadRequest
from .serializers import (
    ItemSerializer,
    LicenseSerializer,
    ItemUploadSerializer,
    PurchaseSerializer,
    MakePurchaseSerializer,
)
from rest_framework.response import Response
from rest_framework import filters
from drf_yasg2 import openapi
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg2.utils import swagger_auto_schema

# Create your views here.
class ItemsView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    throttle_classes = ()
    queryset = Item.objects.all().filter(is_archive=False)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ItemSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ("id", "name", "tags", "owner")
    search_fields = ("name", "tags")
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.pk:
            if instance.is_archive == False and instance.owner.pk == user.pk:
                self.perform_destroy(instance)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return HttpResponseBadRequest()
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def perform_destroy(self, instance):
        instance.delete()

    from rest_framework.decorators import action

    @action(detail=False, methods=["get"])
    @swagger_auto_schema(
        manual_parameters=None,
        request_body=None,
        operation_description="Fetch all tags",
    )
    def tags(self, request, *args, **kwargs):

        all_tags = set()
        for item in self.queryset:
            tags = item.tags.split(";")
            for tag in tags:
                all_tags.add(tag)
        return Response(data=all_tags)


class UploadImageView(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    throttle_classes = ()
    queryset = Item.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemUploadSerializer
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)


class LicenseView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    throttle_classes = ()
    authentication_classes = (TokenAuthentication,)
    serializer_class = LicenseSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    def get_queryset(self):
        from django.db.models import Q

        c1 = Q(default=True)
        c2 = Q(owner__pk=self.request.user.pk)
        return License.objects.all().filter(c1 | c2)

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            self.get_queryset(), context={"request": request}, many=True
        )
        return Response(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(
            instance, context={"request": request}, many=False
        )
        return Response(serializer.data)


class PurchaseView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet,
):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    serializer_class = PurchaseSerializer
    renderer_classes = (renderers.JSONRenderer,)

    def get_queryset(self):
        return Purchase.objects.all().filter(merchant__pk=self.request.user.pk)

    @swagger_auto_schema(
        responses={201: PurchaseSerializer, 400: "Bad request"},
        request_body=MakePurchaseSerializer,
        operation_description="Buy and item",
    )
    def post(self, request, *args, **kwargs):
        serializer = MakePurchaseSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            item = Item.objects.get(pk=serializer.validated_data["item"])
            print(item)
            item.pk = None
            item.save()
            purchase = Purchase()
            purchase.merchant = request.user
            purchase.item = item
            purchase.save()
            return Response(
                data=self.serializer_class(purchase), status=status.HTTP_201_CREATED
            )
            return Response()
        else:
            return HttpResponseBadRequest()


class BuyView(APIView):
    throttle_classes = ()
    permission_classes = ()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    serializer_class = MakePurchaseSerializer
    renderer_classes = (renderers.JSONRenderer,)

    @swagger_auto_schema(
        responses={201: PurchaseSerializer, 400: "Bad request"},
        request_body=MakePurchaseSerializer,
        operation_description="Buy and item",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            item = Item.objects.get(pk=serializer.validated_data["item"].pk)
            item.pk = None
            item.is_archive = True
            item.save()
            purchase = Purchase()
            purchase.merchant = request.user
            purchase.item = item
            purchase.save()
            return Response(
                data=PurchaseSerializer(purchase).data, status=status.HTTP_201_CREATED
            )
        else:
            return HttpResponseBadRequest()
