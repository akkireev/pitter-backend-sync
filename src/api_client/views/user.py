from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import UserPatchRequest, UserPatchResponse, UserDeleteResponse, \
    UserDeleteRequest, AUTH_PARAM, USER_URL_PARAM
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required
from pitter.exceptions import ForbiddenError


class UserMobileView(APIView):
    @classmethod
    @access_token_required
    @request_post_serializer(UserPatchRequest)
    @response_dict_serializer(UserPatchResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=UserPatchRequest,
        manual_parameters=[AUTH_PARAM, USER_URL_PARAM],
        responses={
            200: UserPatchResponse,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Обновление информации об учетной записи',
        operation_description='Обновление информации об учетной записи в сервисе Pitter',
    )
    def patch(cls, request, user_id) -> Dict:
        """
        :param user_id:
        :param request:
        :return:
        """
        if user_id != request.api_user.id:
            raise ForbiddenError()

        new_email = request.data.get('email', None)
        email_notifications_enabled = request.data.get('email_notifications_enabled', None)
        new_profile_name = request.data.get('profile_name', None)

        update_fields = dict()
        if new_email:
            update_fields['email'] = new_email
        if new_profile_name:
            update_fields['profile_name'] = new_profile_name
        if email_notifications_enabled:
            update_fields['email_notifications_enabled'] = email_notifications_enabled

        request.api_user.patch(**update_fields)

        return dict(
            id=request.api_user.id,
            login=request.api_user.login,
            email=request.api_user.email,
            email_notifications_enabled=request.api_user.email_notifications_enabled,
            profile_name=request.api_user.profile_name,
        )

    @classmethod
    @access_token_required
    @request_post_serializer(UserDeleteRequest)
    @response_dict_serializer(UserDeleteResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=UserDeleteRequest,
        manual_parameters=[AUTH_PARAM],
        responses={
            204: UserDeleteResponse,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление учетной записи',
        operation_description='Удаление учетной записи в сервисе Pitter',
    )
    def delete(cls, request, user_id) -> None:
        if user_id != request.api_user.id:
            raise ForbiddenError()
