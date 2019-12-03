from rest_framework import serializers

from pitter.integrations import GoogleSpeechToText


class PittsPostRequest(serializers.Serializer):
    storage_file_path = serializers.CharField(required=True, label='Путь к файлу на удаленном хранилище')
    language_code = serializers.ChoiceField(required=True, label='Код языка для перевода',
                                            choices=GoogleSpeechToText.get_supported_languages())


class PittsPostResponse(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=256, label='ID питта')
    owner_id = serializers.CharField(required=True, max_length=256, label='ID владельца')
    storage_file_path = serializers.CharField(required=True, label='Путь к файлу на удаленном хранилище')
    transcription = serializers.CharField(required=True, label='Распознанный текст')


class PittsGetRequest(serializers.Serializer):
    cursor = serializers.CharField(required=False, label='Текущий cursor')


class PittsGetResponse(serializers.Serializer):
    next = serializers.CharField(required=True, allow_null=True, max_length=256,
                                 label='Cursor для следующих объектов')
    results = serializers.ListField(required=True, label='Текущие pittы')
