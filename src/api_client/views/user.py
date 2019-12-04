from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import UserPatchRequest, UserPatchResponse, UserDeleteResponse, \
    UserDeleteRequest, AUTH_PARAM, USER_URL_PATH_PARAM, UserGetResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer, access_token_required
from pitter.exceptions import ForbiddenError, NotFoundError
from pitter.models import User, Follower


class UserMobileView(APIView):
    @classmethod
    @access_token_required
    @response_dict_serializer(UserGetResponse)
    @swagger_auto_schema(
        tags=['Pitter: userflow'],
        manual_parameters=[USER_URL_PATH_PARAM, AUTH_PARAM],
        responses={
            200: UserGetResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Get info about user',
        operation_description='Get user info. Returns private values as well if provided token is same as user_id',
    )
    def get(cls, request, user_id):
        """
        Get user info. Returns email and email_notification_enabled if token valid for user_id. Else returns
        "following" info
        @param request:
        @param user_id: user's id to get info from
        @return:
        """
        try:
            user = User.get(id=user_id)
        except User.DoesNotExist:
            raise NotFoundError()

        followers_num = user.followers.count()
        following_num = user.targets.count()

        response_dict = user.to_dict()
        response_dict['followers_num'] = followers_num
        response_dict['following_num'] = following_num

        is_my_profile = request.api_user == user
        response_dict['is_my_profile'] = is_my_profile
        response_dict['email'] = user.email if is_my_profile and user.email else None
        response_dict['email_notifications_enabled'] = user.email_notifications_enabled if is_my_profile else None
        response_dict['following'] = None if is_my_profile else Follower.is_following_by(user, request.api_user)

        return response_dict

    @classmethod
    @access_token_required
    @request_post_serializer(UserDeleteRequest)
    @response_dict_serializer(UserDeleteResponse)
    @swagger_auto_schema(
        tags=['Pitter: userflow'],
        request_body=UserDeleteRequest,
        manual_parameters=[AUTH_PARAM, USER_URL_PATH_PARAM],
        responses={
            200: UserDeleteResponse,
            401: exceptions.ExceptionResponse,
            403: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Delete user',
        operation_description='Delete user and his pitts using his token',
    )
    def delete(cls, request, user_id):
        """
        Delete user and all his pitts
        @param request:
        @param user_id: user's id to delete
        @return:
        """
        if user_id != request.api_user.id:
            raise ForbiddenError()

        request.api_user.delete()

        return dict()

    @classmethod
    @access_token_required
    @request_post_serializer(UserPatchRequest)
    @response_dict_serializer(UserPatchResponse)
    @swagger_auto_schema(
        tags=['Pitter: userflow'],
        request_body=UserPatchRequest,
        manual_parameters=[AUTH_PARAM, USER_URL_PATH_PARAM],
        responses={
            200: UserPatchResponse,
            403: exceptions.ExceptionResponse,
            422: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Patch user info',
        operation_description='Patch user info to change email, profile_name etc',
    )
    def patch(cls, request, user_id):
        """
        Patch user info
        @param user_id: user's id to patch
        @param request:
        @return:
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
