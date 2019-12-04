import requests
from django.conf import settings

from pitter import exceptions


class GoogleSpeechToText:
    supported_languages = settings.SPEECH_TO_TEXT_SUPPORTED_LANGUAGES

    @staticmethod
    def recognize_speech(storage_file_path: str, language_code: str = "ru") -> str:
        request_data = {
            'storage_file_path': storage_file_path,
            'language_code': language_code,
        }
        try:
            response = requests.post(settings.SPEECH_TO_TEXT_INTEGRATION_URI, json=request_data)
        except Exception as exc:
            raise exceptions.GoogleSpeechToTextError() from exc

        if response.status_code != 200:
            raise exceptions.GoogleSpeechToTextError()

        return response.json()['speech_transcription']

    @classmethod
    def get_supported_languages(cls):
        return cls.supported_languages
