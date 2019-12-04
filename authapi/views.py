from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    TokenResponseSerializer,
    UserDataSerializer,
)
from django.http import HttpResponseBadRequest
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        responses={200: TokenResponseSerializer},
        operation_description="Request for user authentication token",
        request_body=LoginSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        result = TokenResponseSerializer(token)
        return Response(data=result.data)


class SignUpUser(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = SignUpSerializer

    @swagger_auto_schema(
        responses={201: TokenResponseSerializer, 400: "Bad request"},
        operation_description="Sign up new user",
        request_body=SignUpSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            result = TokenResponseSerializer(token)
            return Response(data=result.data)
        except IntegrityError as e:
            return HttpResponseBadRequest(content=str(e))


class HasPermission(APIView):
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)

    @swagger_auto_schema(
        responses={200: "Authenticated", 401: "Unauthorized"},
        operation_description="Check token validity",
    )
    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class UserData(APIView):
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = UserDataSerializer

    @swagger_auto_schema(
        responses={200: UserDataSerializer, 404: "No such user"},
        operation_description="Get user data",
    )
    def get(self, request, *args, **kwargs):

        if request.user:
            serializer = self.serializer_class(request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={200: UserDataSerializer, 400: "Bad request"},
        operation_description="Update user details",
        request_body=UserDataSerializer,
    )
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            request.user, data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.update(request.user, serializer.validated_data)
            return Response(data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


has_permission = HasPermission.as_view()
sign_up_user = SignUpUser.as_view()
obtain_auth_token = ObtainAuthToken.as_view()
user_data = UserData.as_view()
