from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from pitter.integrations.google_speech_to_text import GoogleSpeechToText
from api_client.validation_serializers import PittPostRequest
from api_client.validation_serializers import PittPostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer


class PittMobileView(APIView):
    parser_classes = [MultiPartParser]

    @classmethod
    @request_post_serializer(PittPostRequest)
    @response_dict_serializer(PittPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=PittPostRequest,
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
        recognized_text: str = GoogleSpeechToText.recognize_speech(request.data['speech_audio'].read())

        return dict(recognized_text=recognized_text,)
