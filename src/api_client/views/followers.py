from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import FollowersPostResponse, FollowersPostRequest, USER_URL_PATH_PARAM, \
    AUTH_PARAM, FollowersGetResponse, FollowersGetRequest

from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required, \
    request_query_serializer
from pitter.exceptions import AlreadyExistsError, ForbiddenError, NotFoundError
from pitter.models import User, Follower
from pitter.utils.smtp_client import SmtpClient


class FollowersMobileView(APIView):
    @classmethod
    @access_token_required
    @request_post_serializer(FollowersPostRequest)
    @response_dict_serializer(FollowersPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: userflow'],
        request_body=FollowersPostRequest,
        manual_parameters=[USER_URL_PATH_PARAM, AUTH_PARAM],
        responses={
            200: FollowersPostResponse,
            401: exceptions.ExceptionResponse,
            403: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Создание подписки',
        operation_description='Создание подписки в сервисе Pitter',
    )
    def post(cls, request, user_id):
        """
        Создание подписки клиентом
        :param user_id:
        :param request:
        :return:
        """
        if user_id != request.api_user.id:
            raise ForbiddenError()

        target_user_id = request.data['following_user_id']
        if user_id == target_user_id:
            raise NotFoundError()

        target_user = User.get(id=target_user_id)

        _, created = Follower.follow(target=target_user, follower=request.api_user)

        if not created:
            raise AlreadyExistsError()
        if target_user.email_notifications_enabled:
            cls.notify_target_user(request.api_user, target_user)
        return dict()

    @classmethod
    def notify_target_user(cls, follower, target):
        msg = f"{follower.login} is now following you!"
        SmtpClient.send_mail(target.email, msg)

    @classmethod
    @access_token_required
    @request_query_serializer(FollowersGetRequest)
    @response_dict_serializer(FollowersGetResponse)
    @swagger_auto_schema(
        tags=['Pitter: userflow'],
        manual_parameters=[USER_URL_PATH_PARAM, AUTH_PARAM],
        responses={
            200: FollowersGetResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Get all followers and following users',
        operation_description='Get all followers and following users from this user_id user',
    )
    def get(cls, request, user_id):
        """
        Get all followers and following users from this user_id
        @param user_id:
        @param request:
        @return:
        """
        try:
            user = User.get(id=user_id)
        except User.DoesNotExist:
            raise NotFoundError()

        followers = Follower.get_user_followers(user)
        followings = Follower.get_user_following_list(user)

        return dict(
            user_id=user.id,
            followers=[follower.to_dict() for follower in followers],
            following=[following.to_dict() for following in followings],
        )
