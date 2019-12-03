from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import PittsPostRequest, PittsPostResponse, AUTH_PARAM, USER_URL_PATH_PARAM, \
    PittsGetResponse, URL_CURSOR_PARAM, PittsGetRequest
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required, \
    request_query_serializer
from pitter.exceptions import ForbiddenError, ValidationError, NotFoundError
from pitter.integrations import GoogleSpeechToText
from pitter.models import Pitt, User
from pitter.utils.cursor_pagination import CursorPagination


class PittsMobileView(APIView):
    @classmethod
    @access_token_required
    @request_post_serializer(PittsPostRequest)
    @response_dict_serializer(PittsPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: pitts'],
        request_body=PittsPostRequest,
        manual_parameters=[AUTH_PARAM, USER_URL_PATH_PARAM],
        responses={
            200: PittsPostResponse,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            409: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Create pitt',
        operation_description='Create pitt using speech_to_text microservice',
    )
    def post(cls, request, user_id) -> Dict:
        """
        Create pitt
        @param user_id: user's id who creates pitt
        @param request:
        @return:
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

        return pitt.to_dict()

    @classmethod
    @access_token_required
    @request_query_serializer(PittsGetRequest)
    @response_dict_serializer(PittsGetResponse)
    @swagger_auto_schema(
        tags=['Pitter: pitts'],
        manual_parameters=[URL_CURSOR_PARAM, USER_URL_PATH_PARAM, AUTH_PARAM],
        responses={
            200: PittsGetResponse,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            409: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Get paginated user pitts',
        operation_description='Get paginated user pitts',
    )
    def get(cls, request, user_id) -> Dict:
        """
        Get paginated user pitts
        @param request:
        @param user_id:
        @return:
        """
        try:
            user = User.get(id=user_id)
        except User.DoesNotExist:
            raise NotFoundError()

        user_pitts_queryset = Pitt.get_user_pitts_queryset(user)

        try:
            pagination = CursorPagination(user_pitts_queryset, request, ['-created_at'])
        except ValueError:
            raise ValidationError()

        current_page_pitts = [pitt.to_dict() for pitt in pagination.get_current_page()]
        return pagination.get_paginated_dict(current_page_pitts)
