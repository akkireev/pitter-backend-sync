from typing import List, Callable

from drf_yasg.openapi import Parameter

from .pitt_serializers import PittPostRequest
from .pitt_serializers import PittPostResponse

from .users_serializers import UsersPostRequest
from .users_serializers import UsersPostResponse


APISPEC_DEFAULT_PARAMS = [
    Parameter(
        name='Authorization',
        in_='header',
        required=True,
        type='string',
    )
]

__all__: List[Callable] = [
    'PittPostRequest',
    'PittPostResponse',
    'UsersPostRequest',
    'UsersPostResponse',
    'APISPEC_DEFAULT_PARAMS',
]
