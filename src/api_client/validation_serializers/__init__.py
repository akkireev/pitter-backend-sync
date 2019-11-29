from typing import List, Callable

from drf_yasg.openapi import Parameter

from .pitt_serializers import PittPostRequest
from .pitt_serializers import PittPostResponse

from .users_serializers import UsersPostRequest
from .users_serializers import UsersPostResponse

from .auth import LoginPostResponse
from .auth import LoginPostRequest
from .auth import LogoutPostRequest
from .auth import LogoutPostResponse

from .user_serializers import UserPatchRequest
from .user_serializers import UserPatchResponse
from .user_serializers import UserDeleteRequest
from .user_serializers import UserDeleteResponse

AUTH_PARAM = Parameter(
    name='Authorization',
    in_='header',
    required=True,
    type='string',
)
USER_URL_PARAM = Parameter(
    name='user_id',
    in_='path',
    required=True,
    type='string',
)

__all__: List[Callable] = [
    'PittPostRequest',
    'PittPostResponse',
    'UsersPostRequest',
    'UsersPostResponse',
    'AUTH_PARAM',
    'USER_URL_PARAM',
    'LoginPostResponse',
    'LoginPostRequest',
    'LogoutPostRequest',
    'LogoutPostResponse',
    'UserPatchRequest',
    'UserPatchResponse',
    'UserDeleteRequest',
    'UserDeleteResponse',
]
