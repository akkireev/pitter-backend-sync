import io
import os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from typing import List

from pitter.exceptions import exceptions
from pitter.utils.audio_handler import AudioHandler

from django.conf import settings


class GoogleSpeechToText:
    @staticmethod
    def convert_audio_codec_to_enum(codec_name: str):
        if codec_name == "pcm_s16le":
            return enums.RecognitionConfig.AudioEncoding.LINEAR16
        # etc
        else:
            raise Exception()

    @staticmethod
    def recognize_speech(filename: str, language_code="ru-RU") -> List[str]:
        # Instantiates a google cloud client
        client = speech.SpeechClient()

        # KLUDGE/TEST: Loads the audio into memory
        # hope we will use blob instead saving file on server
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        with io.open(file_path, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        # Prepare config dynamically
        try:
            audio_info = AudioHandler.get_mediainfo(file_path)
            config = types.RecognitionConfig(
                encoding=GoogleSpeechToText.convert_audio_codec_to_enum(audio_info["codec_name"]),
                audio_channel_count=int(audio_info["channels"]),
                sample_rate_hertz=int(audio_info["sample_rate"]),
                language_code=language_code)
        except Exception as exc:
            raise exceptions.UnsupportedAudioFormatError() from exc

        # Recognize speech using google api
        try:
            response = client.recognize(config, audio)
        except Exception as exc:
            raise exceptions.GoogleSpeechToTextError() from exc

        return [result.alternatives[0].transcript for result in response.results]
