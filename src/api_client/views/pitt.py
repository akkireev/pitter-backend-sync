from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import PittDeleteRequest, AUTH_PARAM, USER_URL_PATH_PARAM, PITT_URL_PATH_PARAM, \
    PittDeleteResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required
from pitter.exceptions import ForbiddenError
from pitter.models import Pitt


class PittMobileView(APIView):
    @classmethod
    @access_token_required
    @request_post_serializer(PittDeleteRequest)
    @response_dict_serializer(PittDeleteResponse)
    @swagger_auto_schema(
        tags=['Pitter: pitts'],
        request_body=PittDeleteRequest,
        manual_parameters=[AUTH_PARAM, USER_URL_PATH_PARAM, PITT_URL_PATH_PARAM],
        responses={
            200: PittDeleteResponse,
            401: exceptions.ExceptionResponse,
            403: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Delete pitt',
        operation_description='Delete pitt from database',
    )
    def delete(cls, request, user_id, pitt_id):
        """
        Delete pitt from database
        @param request:
        @param user_id:
        @param pitt_id:
        @return:
        """
        if user_id != request.api_user.id:
            raise ForbiddenError()

        Pitt.delete_pitt(pitt_id)

        return dict()
