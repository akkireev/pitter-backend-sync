from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import AUTH_PARAM, USER_URL_PATH_PARAM, FollowerDeleteRequest, \
    FollowerDeleteResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required
from pitter.exceptions import ForbiddenError, PitterException
from pitter.models import Follower, User


class FollowerMobileView(APIView):
    @classmethod
    @access_token_required
    @request_post_serializer(FollowerDeleteRequest)
    @response_dict_serializer(FollowerDeleteResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=FollowerDeleteRequest,
        manual_parameters=[AUTH_PARAM, USER_URL_PATH_PARAM],
        responses={
            204: FollowerDeleteResponse,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Удаление подписки',
        operation_description='Удаление подписки в сервисе Pitter',
    )
    def delete(cls, request, user_id, following_user_id) -> Dict:
        if user_id != request.api_user.id:
            raise ForbiddenError()

        target_user_id = User.get(id=following_user_id)

        try:
            Follower.unfollow(target=target_user_id, follower=request.api_user)
        except Exception as exc:
            raise PitterException('Что-то пошло не так', 'ServerError') from exc

        return dict()
