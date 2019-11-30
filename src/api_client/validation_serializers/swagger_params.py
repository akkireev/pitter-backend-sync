from drf_yasg.openapi import Parameter

AUTH_PARAM = Parameter(
    name='Authorization',
    in_='header',
    required=True,
    type='string',
)
USER_URL_PATH_PARAM = Parameter(
    name='user_id',
    in_='path',
    required=True,
    type='string',
)
USERS_URL_FILTER_PARAM = Parameter(
    name='user_id',
    in_='path',
    required=True,
    type='string',
)
