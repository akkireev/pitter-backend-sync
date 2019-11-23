from rest_framework import serializers

from api_client.validation_serializers.validators import LoginValidator, PasswordValidator


class UsersPostRequest(serializers.Serializer):
    login = serializers.CharField(required=True, max_length=64, label='Логин', validators=[LoginValidator.validate])
    password = serializers.CharField(required=True, max_length=64, label='Пароль',
                                     validators=[PasswordValidator.validate])


class UsersPostResponse(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=256)
    login = serializers.CharField(required=True, max_length=64)
