from rest_framework import generics
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from account.serializers import AccountSerializer, AuthTokenSerializer


class CreateAccountView(generics.CreateAPIView):
    serializer_class = AccountSerializer


class ManageAccountView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
