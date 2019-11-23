from __future__ import annotations

from django.db import models

from pitter.models.base import BaseModel
from pitter.models.user import User


class Pitt(BaseModel):
    owner = models.ForeignKey(User, related_name='pitts', on_delete=models.CASCADE)
    speech_audio_file = models.FileField()
    speech_transcription = models.TextField()
