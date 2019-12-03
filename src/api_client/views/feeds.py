from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import USER_URL_PATH_PARAM, \
    FeedsGetResponse, URL_CURSOR_PARAM, AUTH_PARAM, FeedsGetRequest
from pitter import exceptions
from pitter.decorators import response_dict_serializer, access_token_required, request_query_serializer
from pitter.exceptions import ValidationError
from pitter.models import Pitt, Follower, User
from pitter.utils.cursor_pagination import CursorPagination


class FeedsMobileView(APIView):
    @classmethod
    @access_token_required
    @request_query_serializer(FeedsGetRequest)
    @response_dict_serializer(FeedsGetResponse)
    @swagger_auto_schema(
        tags=['Pitter: pitts'],
        manual_parameters=[URL_CURSOR_PARAM, USER_URL_PATH_PARAM, AUTH_PARAM],
        responses={
            200: FeedsGetResponse,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            409: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Get paginated pitts feed for user',
        operation_description='Get paginated pitts feed for user with dynamic load ability',
    )
    def get(cls, request, user_id) -> Dict:
        """
        Get paginated pitts feed for user
        @param request:
        @param user_id:
        @return:
        """
        user = User.get(id=user_id)
        user_followings = Follower.get_user_following_list(user)
        user_followings.append(user)
        user_pitts_queryset = Pitt.get_users_pitts_queryset(user_followings)

        try:
            pagination = CursorPagination(user_pitts_queryset, request, ['-created_at'])
        except ValueError:
            raise ValidationError()

        current_page_pitts = [pitt.to_dict() for pitt in pagination.get_current_page()]
        return pagination.get_paginated_dict(current_page_pitts)
