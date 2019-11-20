from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from pitter import exceptions
from pitter.utils.audio_handler import AudioHandler


class GoogleSpeechToText:
    GOOGLE_SPEECH_CODECS: dict = {
        'audio/flac': enums.RecognitionConfig.AudioEncoding.LINEAR16,
        'audio/x-wav': enums.RecognitionConfig.AudioEncoding.LINEAR16
    }

    @staticmethod
    def recognize_speech(audio_bytes: bytes, language_code="ru-RU") -> str:
        # Instantiates a google cloud client
        client = speech.SpeechClient()
        audio = types.RecognitionAudio(content=audio_bytes)

        # TODO: move to serializers
        # Prepare config dynamically
        try:
            audio_mime_type = AudioHandler.get_mediainfo(audio_bytes)
            config = types.RecognitionConfig(
                encoding=GoogleSpeechToText.GOOGLE_SPEECH_CODECS[audio_mime_type],
                language_code=language_code)
        except Exception as exc:
            raise exceptions.ValidationError(message='Данный формат аудио не поддерживается', status_code=415) from exc

        # Recognize speech using google api
        try:
            response = client.recognize(config, audio)
        except Exception as exc:
            raise exceptions.GoogleSpeechToTextError() from exc

        return '\n'.join([result.alternatives[0].transcript for result in response.results])
