from rest_framework import serializers

from pitter.integrations import GoogleSpeechToText


class PittPostRequest(serializers.Serializer):
    storage_file_path = serializers.CharField(required=True, label='Путь к файлу на удаленном хранилище')
    language_code = serializers.ChoiceField(required=True, label='Код языка для перевода',
                                            choices=GoogleSpeechToText.SUPPORTED_LANGUAGES)


class PittPostResponse(serializers.Serializer):
    transcription = serializers.CharField(required=True, label='Распознанный текст')
