from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.models import Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}
        }

    def create(self, validated_data) -> Account:
        return get_user_model().objects.create_user(**validated_data)


