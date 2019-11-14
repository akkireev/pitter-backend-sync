from rest_framework import serializers
from rest_framework.exceptions import APIException


class ExceptionResponse(serializers.Serializer):
    code = serializers.CharField(required=True)
    title = serializers.CharField(required=False, allow_null=True)
    message = serializers.CharField(required=True)
    payload = serializers.DictField(required=False, allow_null=True)
    debug = serializers.CharField(required=False, allow_null=True)


class PitterException(APIException):
    default_detail = 'Something went wrong.'
    default_code = 'ServerError'

    def __init__(self, message, error_code, status_code=500):
        detail = message
        super().__init__(detail, error_code)
        self.status_code = status_code

    @staticmethod
    def get_exception_serializer():
        """

        :return:
        """
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
        super().__init__(detail, exception_code)
