from django.urls import path
from .views import obtain_auth_token, sign_up_user, has_permission, user_data

urlpatterns = [
    path("signup/", sign_up_user, name="api_sign_up"),
    path("token/", obtain_auth_token, name="api_token_auth"),
    path("permission/", has_permission, name="api_has_permission"),
    path("user/", user_data, name="api_user_data"),
]
