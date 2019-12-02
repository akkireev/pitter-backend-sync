from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import PittsPostRequest, PittsPostResponse, AUTH_PARAM, USER_URL_PATH_PARAM
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter.exceptions import ForbiddenError
from pitter.integrations import GoogleSpeechToText
from pitter.models import Pitt


class PittsMobileView(APIView):
    @classmethod
    @request_post_serializer(PittsPostRequest)
    @response_dict_serializer(PittsPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=PittsPostRequest,
        manual_parameters=[AUTH_PARAM, USER_URL_PATH_PARAM],
        responses={
            201: PittsPostResponse,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            409: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Создание pitt',
        operation_description='Создание pitt в сервисе Pitter',
    )
    def post(cls, request, user_id) -> Dict:
        """
        Создание pitt
        :param user_id:
        :param request:
        :return:
        """
        if user_id != request.api_user.id:
            raise ForbiddenError()

        storage_file_path = request.data['storage_file_path']
        language_code = request.data['language_code']

        transcription: str = GoogleSpeechToText.recognize_speech(
            storage_file_path=storage_file_path,
            language_code=language_code,
        )

        pitt = Pitt.create_pitt(request.api_user, storage_file_path, transcription)

        return dict(
            id=pitt.id,
            storage_file_path=pitt.speech_audio_file_path,
            transcription=pitt.speech_transcription,
        )
