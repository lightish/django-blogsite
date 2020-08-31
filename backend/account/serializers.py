from django.contrib.auth import get_user_model, authenticate
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

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        account = super().update(instance, validated_data)

        if password:
            account.set_password(password)
            account.save()

        return account


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['email'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError(
                'Unable to authenticate with provided credentials',
                code='authentication'
            )

        attrs['user'] = user
        return attrs
