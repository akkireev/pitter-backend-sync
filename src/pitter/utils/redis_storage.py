import datetime

import redis
from django.conf import settings


class RedisStorage:
    redis_session = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                db=settings.REDIS_DB_NUMBER, password=settings.REDIS_PASSWORD)

    @classmethod
    def delete_token(cls, user_id):
        return cls.redis_session.delete(user_id) == 1

    @classmethod
    def set_token(cls, user_id, token, expiration_time: datetime.timedelta = None):
        if expiration_time:
            return cls.redis_session.setex(user_id, expiration_time, token)
        return cls.redis_session.set(user_id, token)

    @classmethod
    def get_token(cls, user_id):
        return cls.redis_session.get(user_id)

    @classmethod
    def check_token_exists(cls, user_id):
        return cls.redis_session.exists(user_id) == 1
