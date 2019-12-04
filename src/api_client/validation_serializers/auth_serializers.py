from rest_framework import serializers


class LoginPostRequest(serializers.Serializer):
    login = serializers.CharField(required=True, max_length=64, label='Логин')
    password = serializers.CharField(required=True, max_length=64, label='Пароль')


class LoginPostResponse(serializers.Serializer):
    user_id = serializers.CharField(required=True, max_length=256, label='ID пользователя')
    token = serializers.CharField(required=True, label='JWT токен')


class LogoutPostRequest(serializers.Serializer):
    pass


class LogoutPostResponse(serializers.Serializer):
    pass
