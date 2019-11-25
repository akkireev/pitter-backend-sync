import datetime

import jwt
from typing import Optional

from django.conf import settings

from pitter.exceptions import AccessTokenInvalid
from pitter.models import User


def check_token(auth_type: str, token: str) -> Optional[dict]:
    """
    Проверяет JWT токен
    :param auth_type:
    :param token:
    :return:
    """
    try:
        if auth_type == 'Bearer':
            decoded = jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=['RS256'])
        else:
            raise
    except Exception:
        raise AccessTokenInvalid()

    return User.get(id=decoded['user_id'])


def create_token(user: User):
    jwt_payload = {
        'user_id': user.id,
        'user_login': user.login,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10)
    }

    return jwt.encode(
        jwt_payload,
        settings.JWT_PRIVATE_KEY,
        algorithm='RS256'
    )
