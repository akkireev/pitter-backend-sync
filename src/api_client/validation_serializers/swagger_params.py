from drf_yasg.openapi import Parameter

from pitter.utils.cursor_pagination import CursorPagination

AUTH_PARAM = Parameter(
    name='Authorization',
    in_='header',
    required=True,
    type='string',
)

URL_CURSOR_PARAM = Parameter(
    name=CursorPagination.cursor_query_param,
    in_='query',
    required=False,
    type='string',
)

USER_URL_PATH_PARAM = Parameter(
    name='user_id',
    in_='path',
    required=True,
    type='string',
)

USERS_URL_FILTER_PARAM = Parameter(
    name='login',
    in_='query',
    required=False,
    type='string',
)

FOLLOWING_USER_URL_PATH_PARAM = Parameter(
    name='following_user_id',
    in_='path',
    required=True,
    type='string',
)