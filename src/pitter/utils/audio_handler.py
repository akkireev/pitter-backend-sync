import base64

from pydub.utils import mediainfo


class AudioHandler:
    @staticmethod
    def get_mediainfo(audio_path):
        return mediainfo(audio_path)

    @staticmethod
    def encode_audio_to_base64(audio):
        audio_content = audio.read()
        return base64.b64encode(audio_content)
