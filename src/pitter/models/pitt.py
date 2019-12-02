from __future__ import annotations

from django.conf import settings
from django.db import models

from pitter.exceptions import TranscriptionIsEmptyError, TranscriptionTooBigError
from pitter.models.base import BaseModel
from pitter.models.user import User


class Pitt(BaseModel):
    owner = models.ForeignKey(User, related_name='pitts', on_delete=models.CASCADE)
    speech_audio_file_path = models.CharField(blank=False, max_length=512)
    speech_transcription = models.TextField(blank=False)

    def to_dict(self):
        return dict(
            id=self.id,
            owner_id=self.owner.id,
            storage_file_path=self.speech_audio_file_path,
            transcription=self.speech_transcription,
        )

    @staticmethod
    def create_pitt(user_id, speech_audio_file_path, speech_transcription):
        Pitt.check_transcription(speech_transcription)

        return Pitt.objects.create(
            owner=user_id,
            speech_audio_file_path=speech_audio_file_path,
            speech_transcription=speech_transcription,
        )

    @staticmethod
    def check_transcription(speech_transcription):
        if len(speech_transcription) <= 0:
            raise TranscriptionIsEmptyError()
        if len(speech_transcription) > settings.SPEECH_TRANSCRIPTION_MAX_LENGTH:
            raise TranscriptionTooBigError()

    @staticmethod
    def delete_pitt(pitt_id):
        Pitt.objects.filter(id=pitt_id).delete()

    @staticmethod
    def get_users_pitts(users):
        return Pitt.objects.filter(owner__in=users).all()
