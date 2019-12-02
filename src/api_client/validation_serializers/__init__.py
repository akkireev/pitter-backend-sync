from typing import List, Callable

from .swagger_params import AUTH_PARAM
from .swagger_params import USER_URL_PATH_PARAM
from .swagger_params import USERS_URL_FILTER_PARAM
from .swagger_params import URL_CURSOR_PARAM
from .swagger_params import PITT_URL_PATH_PARAM

from .pitt_serializers import PittDeleteRequest
from .pitt_serializers import PittDeleteResponse

from .users_serializers import UsersPostRequest
from .users_serializers import UsersPostResponse
from .users_serializers import UsersGetRequest
from .users_serializers import UsersGetResponse

from .auth_serializers import LoginPostResponse
from .auth_serializers import LoginPostRequest
from .auth_serializers import LogoutPostRequest
from .auth_serializers import LogoutPostResponse

from .user_serializers import UserPatchRequest
from .user_serializers import UserPatchResponse
from .user_serializers import UserDeleteRequest
from .user_serializers import UserDeleteResponse

from .followers_serializers import FollowersPostRequest
from .followers_serializers import FollowersPostResponse

from .follower_serializers import FollowerDeleteRequest
from .follower_serializers import FollowerDeleteResponse

from .pitts_serializers import PittsPostRequest
from .pitts_serializers import PittsPostResponse

__all__: List[Callable] = [
    # swagger
    'AUTH_PARAM',
    'USERS_URL_FILTER_PARAM',
    'USER_URL_PATH_PARAM',
    'URL_CURSOR_PARAM',
    'PITT_URL_PATH_PARAM',

    # serializers
    'PittDeleteRequest',
    'PittDeleteResponse',
    'UsersPostRequest',
    'UsersPostResponse',
    'AUTH_PARAM',
    'USER_URL_PATH_PARAM',
    'LoginPostResponse',
    'LoginPostRequest',
    'LogoutPostRequest',
    'LogoutPostResponse',
    'UserPatchRequest',
    'UserPatchResponse',
    'UserDeleteRequest',
    'UserDeleteResponse',
    'UsersGetRequest',
    'UsersGetResponse',
    'FollowersPostRequest',
    'FollowersPostResponse',
    'FollowerDeleteRequest',
    'FollowerDeleteResponse',
    'PittsPostResponse',
    'PittsPostRequest',
]
