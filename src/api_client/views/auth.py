import datetime
from typing import Dict

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import AUTH_PARAM, LoginPostRequest, LoginPostResponse, \
    LogoutPostRequest, LogoutPostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required
from pitter.exceptions import InvalidCredentialsError
from pitter.models import User
from pitter.utils.auth import JwtTokenAuth
from pitter.utils.redis_storage import RedisStorage


class LoginMobileView(APIView):
    @classmethod
    @request_post_serializer(LoginPostRequest)
    @response_dict_serializer(LoginPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: userflow'],
        request_body=LoginPostRequest,
        responses={
            200: LoginPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Login в сервисе',
        operation_description='Login в сервисе Pitter',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        :param request:
        :return:
        """
        login = request.data['login']
        password = request.data['password']

        user = cls.check_user_credentials(login, password)
        token = cls.create_token(user)

        return dict(
            user_id=user.id,
            token=token,
        )

    @classmethod
    def check_user_credentials(cls, login, password) -> User:
        try:
            user = User.get(login=login)
        except User.DoesNotExist:
            raise InvalidCredentialsError()
        if not user.check_password(password):
            raise InvalidCredentialsError()

        return user

    @classmethod
    def create_token(cls, user: User) -> str:
        timedelta = datetime.timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)
        token = JwtTokenAuth.create_user_token(user, timedelta)
        RedisStorage.delete_token(user.id)
        RedisStorage.set_token(user.id, token, timedelta)

        return token


class LogoutMobileView(APIView):
    @classmethod
    @access_token_required
    @request_post_serializer(LogoutPostRequest)
    @response_dict_serializer(LogoutPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: userflow'],
        request_body=LogoutPostRequest,
        manual_parameters=[AUTH_PARAM],
        responses={
            200: LogoutPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            415: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Logout из сервиса',
        operation_description='Logout из сервиса Pitter',
    )
    def post(cls, request) -> Dict:
        """
        :param request:
        :return:
        """
        RedisStorage.delete_token(request.api_user.id)

        return dict()
