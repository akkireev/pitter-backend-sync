import base64
import magic


class AudioHandler:
    @staticmethod
    def get_mediainfo(audio_bytes: bytes):
        return magic.from_buffer(audio_bytes, mime=True)

    @staticmethod
    def encode_audio_to_base64(audio_bytes: bytes):
        return base64.b64encode(audio_bytes)
