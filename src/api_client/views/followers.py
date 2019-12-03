from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import FollowersPostResponse, FollowersPostRequest, USER_URL_PATH_PARAM, \
    AUTH_PARAM

from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required
from pitter.exceptions import AlreadyExistsError, ForbiddenError
from pitter.models import User, Follower


class FollowersMobileView(APIView):
    @classmethod
    @access_token_required
    @request_post_serializer(FollowersPostRequest)
    @response_dict_serializer(FollowersPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=FollowersPostRequest,
        manual_parameters=[USER_URL_PATH_PARAM, AUTH_PARAM],
        responses={
            200: FollowersPostResponse,
            401: exceptions.ExceptionResponse,
            403: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Создание подписки',
        operation_description='Создание подписки в сервисе Pitter',
    )
    def post(cls, request, user_id) -> Dict:
        """
        Создание подписки клиентом
        :param user_id:
        :param request:
        :return:
        """
        if user_id != request.api_user.id:
            raise ForbiddenError()

        following_user_id = request.data['following_user_id']
        target_user_id = User.get(id=following_user_id)

        _, created = Follower.follow(target=target_user_id, follower=request.api_user)

        if created:
            return dict()
        else:
            raise AlreadyExistsError()
