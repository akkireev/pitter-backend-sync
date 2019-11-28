import requests
from django.conf import settings

from pitter import exceptions


class GoogleSpeechToText:
    SUPPORTED_LANGUAGES = ['ru', 'en']
    @staticmethod
    def recognize_speech(storage_file_path: str, language_code="ru") -> str:
        request_data = {
            'storage_file_path': storage_file_path,
            'language_code': language_code,
        }
        try:
            response = requests.post(settings.SPEECH_TO_TEXT_INTEGRATION_URI, json=request_data)
            print(response)
            if response.status_code == 200:
                return response.json()['speech_transcription']
            raise
        except Exception as exc:
            raise exceptions.GoogleSpeechToTextError() from exc
