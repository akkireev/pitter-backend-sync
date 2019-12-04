from rest_framework import serializers


class FeedsGetRequest(serializers.Serializer):
    cursor = serializers.CharField(required=False, label='Текущий cursor')


class FeedsGetResponse(serializers.Serializer):
    next = serializers.CharField(required=True, allow_null=True, max_length=256, label='Cursor для следующих объектов')
    results = serializers.ListField(required=True, label='Текущие pittы')
