from rest_framework import parsers, renderers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, mixins
from rest_framework.viewsets import GenericViewSet
from .models import Item
from rest_framework.authentication import TokenAuthentication
from .serializers import ItemSerializer
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

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
    permission_classes = (IsAuthenticated,)
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
