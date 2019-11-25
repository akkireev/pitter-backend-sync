from pitter.exceptions import AuthTypeInvalid, AccessTokenInvalid
from django.utils.deprecation import MiddlewareMixin

from pitter.middleware import custom_middleware_exception
from pitter.utils.auth import check_token


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth = request.headers.get('Authorization', '').split()

        if not auth:
            return

        if len(auth) != 2:
            return custom_middleware_exception(AuthTypeInvalid())

        auth_type = auth[0]
        token = auth[1]

        try:
            user = check_token(auth_type, token)
        except AccessTokenInvalid as exc:
            return custom_middleware_exception(exc)

        setattr(request, 'api_user', user)
