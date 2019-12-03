from rest_framework import serializers

from api_client.validation_serializers.validators import LoginValidator, PasswordValidator


class UsersPostRequest(serializers.Serializer):
    login = serializers.CharField(required=True, max_length=64, label='Логин', validators=[LoginValidator.validate])
    password = serializers.CharField(required=True, max_length=64, label='Пароль',
                                     validators=[PasswordValidator.validate])


class UsersPostResponse(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=256)
    login = serializers.CharField(required=True, max_length=64)


class UsersGetRequest(serializers.Serializer):
    cursor = serializers.CharField(required=False, label='Текущий cursor')
    login = serializers.CharField(required=False, max_length=64, label='Login для поиска в пользователях')


class UsersGetResponse(serializers.Serializer):
    next = serializers.CharField(required=True, allow_null=True, max_length=256, label='Cursor для следующих объектов')
    results = serializers.ListField(required=True, label='Текущие пользователи')
