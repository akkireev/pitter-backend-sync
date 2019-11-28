import functools

from pitter.exceptions import AccessTokenInvalid


def access_token_required(handler):
    @functools.wraps(handler)
    def _wrapper(view, request, *args, **kwargs):
        if not getattr(request, 'api_user', None):
            raise AccessTokenInvalid()
        return handler(view, request, *args, **kwargs)

    return _wrapper
