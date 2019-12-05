from rest_framework import parsers, renderers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, mixins
from rest_framework.viewsets import GenericViewSet
from .models import Item, License
from rest_framework.authentication import TokenAuthentication
from .serializers import ItemSerializer, LicenseSerializer, ItemUploadSerializer
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class ItemsView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet,
):
    throttle_classes = ()
    queryset = Item.objects.all()
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

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            self.queryset, context={"request": request}, many=True
        )
        return Response(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.image.path)
        serializer = ItemSerializer(instance, context={"request": request}, many=False)
        return Response(serializer.data)


class UploadImageView(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    throttle_classes = ()
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
