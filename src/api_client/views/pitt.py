from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import PittDeleteRequest, AUTH_PARAM, USER_URL_PATH_PARAM, PITT_URL_PATH_PARAM, \
    PittDeleteResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required
from pitter.exceptions import ForbiddenError, PitterException
from pitter.models import Pitt


class PittMobileView(APIView):
    @classmethod
    @access_token_required
    @request_post_serializer(PittDeleteRequest)
    @response_dict_serializer(PittDeleteResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=PittDeleteRequest,
        manual_parameters=[AUTH_PARAM, USER_URL_PATH_PARAM, PITT_URL_PATH_PARAM],
        responses={
            204: PittDeleteResponse,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление pitt',
        operation_description='Удаление pitt в сервисе Pitter',
    )
    def delete(cls, request, user_id, pitt_id) -> Dict:
        if user_id != request.api_user.id:
            raise ForbiddenError()

        try:
            Pitt.delete_pitt(pitt_id)
        except Exception as exc:
            raise PitterException('Что-то пошло не так', 'ServerError') from exc

        return dict()
