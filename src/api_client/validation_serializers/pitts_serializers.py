from rest_framework import serializers

from pitter.integrations import GoogleSpeechToText


class PittsPostRequest(serializers.Serializer):
    storage_file_path = serializers.CharField(required=True, label='Путь к файлу на удаленном хранилище')
    language_code = serializers.ChoiceField(required=True, label='Код языка для перевода',
                                            choices=GoogleSpeechToText.SUPPORTED_LANGUAGES)


class PittsPostResponse(serializers.Serializer):
    id = serializers.CharField(required=True, max_length=256, label='ID питта')
    storage_file_path = serializers.CharField(required=True, label='Путь к файлу на удаленном хранилище')
    transcription = serializers.CharField(required=True, label='Распознанный текст')
