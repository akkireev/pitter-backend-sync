from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import UsersPostRequest, UsersPostResponse, UsersGetResponse, UsersGetRequest, \
    URL_CURSOR_PARAM, USERS_URL_FILTER_PARAM, AUTH_PARAM

from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required
from pitter.exceptions import AlreadyExistsError, ValidationError
from pitter.models import User
from pitter.utils.cursor_pagination import CursorPagination


class UsersMobileView(APIView):
    @classmethod
    @request_post_serializer(UsersPostRequest)
    @response_dict_serializer(UsersPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: userflow'],
        request_body=UsersPostRequest,
        responses={
            200: UsersPostResponse,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            409: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Создание учетной записи',
        operation_description='Создание учетной записи в сервисе Pitter',
    )
    def post(cls, request) -> Dict:
        """
        Создание учетной записи клиентом
        :param request:
        :return:
        """
        login: str = request.data['login']
        password: str = request.data['password']

        user, registered = User.register_new_user(
            login=login,
            password=password
        )

        if registered:
            return dict(
                id=user.id,
                login=user.login
            )

        else:
            raise AlreadyExistsError(
                message="Пользователь с таким логином уже существует",
                status_code=409,
                payload={'field_name': 'login'}
            )

    @classmethod
    @access_token_required
    @response_dict_serializer(UsersGetResponse)
    @swagger_auto_schema(
        tags=['Pitter: userflow'],
        manual_parameters=[URL_CURSOR_PARAM, USERS_URL_FILTER_PARAM, AUTH_PARAM],
        responses={
            200: UsersGetResponse,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            409: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Получение списка пользователей',
        operation_description='Получение списка пользователей в сервисе Pitter',
    )
    def get(cls, request) -> Dict:
        """
        Получения списка пользователей
        :param request:
        :return:
        """
        login_filter = request.query_params.get('login', None)

        users_queryset = User.objects
        if login_filter:
            users_queryset = users_queryset.filter(login__contains=login_filter)

        paginator = CursorPagination()
        try:
            current_page_data = paginator.paginate_queryset(users_queryset, request, ['-joined_at'])
        except ValueError:
            raise ValidationError()

        current_page_users = [user.to_dict() for user in current_page_data]
        return paginator.get_paginated_dict(current_page_users)
