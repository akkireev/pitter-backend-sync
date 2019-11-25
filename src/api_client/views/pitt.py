from typing import Dict

from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import PittPostRequest, APISPEC_DEFAULT_PARAMS
from api_client.validation_serializers import PittPostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required
from pitter.integrations import GoogleSpeechToText


class PittMobileView(APIView):
    @classmethod
    @access_token_required
    @request_post_serializer(PittPostRequest)
    @response_dict_serializer(PittPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=PittPostRequest,
        manual_parameters=APISPEC_DEFAULT_PARAMS,
        responses={
            200: PittPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Создание pitta',
        operation_description='Создание pitta в сервисе Pitter',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        Создание pitt'a клиентом
        :param request:
        :return:
        """
        transcription: str = GoogleSpeechToText.recognize_speech(
            storage_file_path=request.data['storage_file_path'],
            language_code=request.data['language_code'],
        )

        return dict(transcription=transcription, )
