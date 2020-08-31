from rest_framework import generics

from account.serializers import AccountSerializer


class CreateAccountView(generics.CreateAPIView):
    serializer_class = AccountSerializer
