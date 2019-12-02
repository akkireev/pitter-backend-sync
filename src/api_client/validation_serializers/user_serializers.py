from rest_framework import serializers

from api_client.validation_serializers.validators import EmailValidator


class UserPatchRequest(serializers.Serializer):
    email = serializers.CharField(required=False, max_length=64, label='Новый e-mail',
                                  validators=[EmailValidator.validate])
    email_notifications_enabled = serializers.BooleanField(required=False, label='Включить уведомления')
    profile_name = serializers.CharField(required=False, max_length=64, label='Новое имя профиля')


class UserPatchResponse(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=256)
    login = serializers.CharField(required=True, max_length=64)
    email = serializers.CharField(required=True, allow_blank=True, max_length=64, label='e-mail')
    email_notifications_enabled = serializers.BooleanField(required=True, label='Включены ли уведомления')
    profile_name = serializers.CharField(required=True, allow_blank=True, max_length=64, label='Имя профиля')


class UserDeleteRequest(serializers.Serializer):
    pass


class UserDeleteResponse(serializers.Serializer):
    pass


class UserGetResponse(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=256)
    login = serializers.CharField(required=True, max_length=64)
    profile_name = serializers.CharField(required=True, allow_blank=True, max_length=64, label='Имя профиля')
    followers_num = serializers.IntegerField(required=True, label='Кол-во фоловеров')
    following_num = serializers.IntegerField(required=True, label='Кол-во людей, на которых подписан')
