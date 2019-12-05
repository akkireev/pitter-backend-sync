from rest_framework import serializers
from rest_framework.exceptions import APIException


class ExceptionResponse(serializers.Serializer):
    code = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_null=True)
    message = serializers.CharField(required=True)
    payload = serializers.DictField(required=False, allow_null=True)
    debug = serializers.CharField(required=False, allow_null=True)


class PitterException(APIException):
    default_detail = 'Something goes wrong'
    default_code = 'ServerError'

    def __init__(self, message, error_code, status_code=500):
        detail = message
        super().__init__(detail, error_code)
        self.status_code = status_code

    @staticmethod
    def get_exception_serializer():
        return ExceptionResponse


class ValidationError(PitterException):
    default_detail = 'Validation error'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 422
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class InternalRequestError(PitterException):
    default_detail = 'Internal requests returned an error'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 401
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code)


class GoogleSpeechToTextError(PitterException):
    default_detail = 'Service GoogleSpeechToText unavailable'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 500
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code)


class AlreadyExistsError(PitterException):
    default_detail = 'Data already exists'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 401
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class AccessTokenInvalid(PitterException):
    default_detail = 'Invalid token'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 401
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class AuthTypeInvalid(PitterException):
    default_detail = 'Invalid authorization type'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 401
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class InvalidCredentialsError(PitterException):
    default_detail = 'Invalid username or password'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 401
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class ForbiddenError(PitterException):
    default_detail = 'Access denied'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 403
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class TranscriptionIsEmptyError(PitterException):
    default_detail = 'Transcription is empty'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 400
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class TranscriptionTooBigError(PitterException):
    default_detail = 'Transcription is too long'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 400
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)


class NotFoundError(PitterException):
    default_detail = 'Not found'

    def __init__(self, message=None, title=None, payload=None, status_code=None):
        detail = message if message else self.default_detail
        exception_code = self.__class__.__name__
        self.default_detail = message if message else self.default_detail
        self.status_code = status_code if status_code else 404
        self.title = title
        self.payload = payload
        super().__init__(detail, exception_code, self.status_code)
