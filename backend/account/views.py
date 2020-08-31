from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from account.serializers import AccountSerializer, AuthTokenSerializer


class CreateAccountView(generics.CreateAPIView):
    serializer_class = AccountSerializer


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
