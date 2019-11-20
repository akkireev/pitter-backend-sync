from rest_framework import serializers


class TicketPostRequest(serializers.Serializer):
    message = serializers.CharField(required=True, label='Сообщение')
    userComment = serializers.CharField(required=False, label='Комментарий пользователя', allow_null=True)


class TicketPostResponse(serializers.Serializer):
    fakeId = serializers.CharField(required=True, label='Фэйковый идентификатор заявки')
    message = serializers.CharField(required=True, label='Сообщение')
    userComment = serializers.CharField(required=False, label='Комментарий пользователя', allow_blank=True)
