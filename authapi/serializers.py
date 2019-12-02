from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _


class TokenResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ("key",)


class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=20)

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data["email"],
            validated_data["email"],
            validated_data["password"],
        )

    def update(self, instance, validated_data):
        instance.username = validated_data.get("email", instance.email)
        instance.email = validated_data.get("email", instance.email)
        instance.save()
        return instance


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
