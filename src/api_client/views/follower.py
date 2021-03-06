from typing import Dict

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import AUTH_PARAM, USER_URL_PATH_PARAM, FollowerDeleteRequest, \
    FollowerDeleteResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required
from pitter.exceptions import ForbiddenError, NotFoundError
from pitter.models import Follower, User


class FollowerMobileView(APIView):
    @classmethod
    @access_token_required
    @request_post_serializer(FollowerDeleteRequest)
    @response_dict_serializer(FollowerDeleteResponse)
    @swagger_auto_schema(
        tags=['Pitter: userflow'],
        request_body=FollowerDeleteRequest,
        manual_parameters=[AUTH_PARAM, USER_URL_PATH_PARAM],
        responses={
            200: FollowerDeleteResponse,
            401: exceptions.ExceptionResponse,
            403: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Unfollow',
        operation_description='Unfollow user',
    )
    def delete(cls, request, user_id, following_user_id) -> Dict:
        """
        Unfollow following user who has following_user_id by user with user_id
        @param request:
        @param user_id:
        @param following_user_id:
        @return:
        """
        if user_id != request.api_user.id:
            raise ForbiddenError()

        try:
            target_user_id = User.get(id=following_user_id)
        except User.DoesNotExist:
            raise NotFoundError()

        Follower.unfollow(target=target_user_id, follower=request.api_user)

        return dict()
