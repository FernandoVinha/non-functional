# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from .models import User

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("The passwords don't match")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TokenRegistrationSerializer(serializers.Serializer):
    token = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user, token = User.objects.create_user_with_token()
        user.set_password(validated_data['password'])
        user.save()
        return {'token': token}

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    token = serializers.UUIDField(required=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        token = data.get('token')
        password = data.get('password')

        if email:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("E-mail ou senha incorretos.")
        elif token:
            try:
                user = User.objects.get(access_token=token)
                if not user.check_password(password):
                    raise serializers.ValidationError("Senha incorreta.")
            except User.DoesNotExist:
                raise serializers.ValidationError("Token inválido.")
        else:
            raise serializers.ValidationError("E-mail ou token é necessário para login.")

        return data


class ReferralLinkSerializer(serializers.Serializer):
    referral_link = serializers.CharField()