from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import UsersPostRequest, UsersPostResponse, UsersGetResponse, \
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
        operation_summary='Create new user',
        operation_description='Create new user and return his id',
    )
    def post(cls, request) -> Dict:
        """
        Create new user entity using login and password
        @param request:
        @return: user_id and his login as dict
        """
        login: str = request.data['login']
        password: str = request.data['password']

        user, registered = User.register_new_user(
            login=login,
            password=password
        )

        if not registered:
            raise AlreadyExistsError(
                message="User with this login already exists",
                status_code=409,
                payload={'field_name': 'login'}
            )

        return dict(
            id=user.id,
            login=user.login
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
        operation_summary='Get paginated users list',
        operation_description='Get paginated users list with link to request more',
    )
    def get(cls, request) -> Dict:
        """
        Get users list with ability to filter by login using login__contains
        @param request:
        @return: return api_settings.PAGE_SIZE users and next link to get more users if they exist, if not - null
        """
        login_filter = request.query_params.get('login', None)

        users_queryset = User.objects
        if login_filter:
            users_queryset = users_queryset.filter(login__contains=login_filter)

        try:
            pagination = CursorPagination(users_queryset, request, ['-joined_at'])
        except ValueError:
            raise ValidationError()

        current_page_users = [user.to_dict() for user in pagination.get_current_page()]
        return pagination.get_paginated_dict(current_page_users)
