from rest_framework import serializers


class RegistrationPostRequest(serializers.Serializer):
    login = serializers.CharField(required=True, max_length=64, label='Логин')
    password = serializers.CharField(required=True, max_length=64, label='Пароль')
