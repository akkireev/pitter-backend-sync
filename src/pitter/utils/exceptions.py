from rest_framework.exceptions import APIException


class PitterException(APIException):
    default_detail = 'Something went wrong.'
    default_code = 'unknown_error'

    def __init__(self, detail=None, code=None, status=500):
        if code:
            detail = detail or ERRORS.get(code)
        super().__init__(detail, code)
        self.status_code = status


ERRORS = dict(
    TokenNotFound='There is no token',
    AccessTokenExpired='There is no token',
    AccessTokenNotVerified='There is no token',
    AccessTokenInvalid='There is no token',
    AuthTypeInvalid='There is no token',
    ServerResponseValidationError='Validation error',
)
