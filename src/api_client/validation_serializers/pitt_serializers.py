from rest_framework import serializers


class PittPostRequest(serializers.Serializer):
    speech_audio = serializers.FileField(required=True, label='Голосовое сообщение')


class PittPostResponse(serializers.Serializer):
    recognized_text = serializers.CharField(required=True, label='Распознанный текст')
