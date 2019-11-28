from pitter.exceptions import AuthTypeInvalid, AccessTokenInvalid
from django.utils.deprecation import MiddlewareMixin

from pitter.middleware import custom_middleware_exception
from pitter.models import User
from pitter.utils.auth import JwtTokenAuth
from pitter.utils.redis_storage import RedisStorage


class AuthenticationMiddleware(MiddlewareMixin):
    redis_storage = RedisStorage()

    def process_request(self, request):
        auth = request.headers.get('Authorization', '').split()
        if not auth:
            return

        if len(auth) != 2:
            return custom_middleware_exception(AuthTypeInvalid())

        auth_type = auth[0]
        token = auth[1]

        try:
            decoded_token = JwtTokenAuth.check_token(auth_type, token)
        except AccessTokenInvalid as exc:
            return custom_middleware_exception(exc)

        user_id = decoded_token['user_id']

        if not self.check_token_in_whitelist(user_id, token):
            return custom_middleware_exception(AccessTokenInvalid())

        user = User.get(id=user_id)
        setattr(request, 'api_user', user)

    def check_token_in_whitelist(self, user_id, token):
        existing_token = self.redis_storage.get_token(user_id)

        # TODO: does better way exist?
        if existing_token is not None:
            return token == existing_token.decode('utf-8')
        return False
