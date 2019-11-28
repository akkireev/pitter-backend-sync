import datetime

import jwt
from typing import Optional

from django.conf import settings

from pitter.exceptions import AccessTokenInvalid
from pitter.models import User


class JwtTokenAuth:
    @classmethod
    def check_token(cls, auth_type: str, token: str) -> Optional[dict]:
        """
        Проверяет JWT токен: валидный ли он
        :param auth_type:
        :param token:
        :return:
        """
        if auth_type != 'Bearer':
            raise AccessTokenInvalid()

        try:
            decoded = jwt.decode(token.encode('utf-8'), settings.JWT_PUBLIC_KEY, algorithms=['RS256'])
        except Exception:
            raise AccessTokenInvalid()

        return decoded

    @classmethod
    def create_user_token(cls, user: User, exp: datetime.timedelta):
        jwt_payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + exp
        }

        return jwt.encode(
            jwt_payload,
            settings.JWT_PRIVATE_KEY,
            algorithm='RS256'
        ).decode('utf-8')
