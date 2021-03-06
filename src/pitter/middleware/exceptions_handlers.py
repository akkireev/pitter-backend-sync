import logging
import traceback
from typing import Optional

from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import exception_handler

from pitter.exceptions import exceptions

LOGGER = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception) -> Optional[JsonResponse]:  # pylint: disable=no-self-use
        if not isinstance(exception, exceptions.PitterException):
            LOGGER.exception(traceback.format_exc())
            return JsonResponse(
                dict(
                    code='ServerError',
                    title='Что-то пошло не так',
                    message=str(exception),
                    debug=traceback.format_exc() if settings.DEBUG else None,
                ),
                status=500,
            )

        return None


def custom_middleware_exception(exception):
    if settings.DEBUG:
        LOGGER.exception(exception)
    return JsonResponse(
        dict(
            code=exception.default_code,
            title=exception.default_detail,
            message=exception.default_detail,
            payload=exception.payload,
            debug=str(exception) if settings.DEBUG else None,
        ),
        status=exception.status_code,
    )


def custom_exception_handler(exception, context):
    response = exception_handler(exception, context)

    if settings.DEBUG:
        LOGGER.exception(traceback.format_exc())

    if isinstance(exception, AssertionError):
        return JsonResponse(
            dict(
                code='ValidationError',
                title='Ошибка валидации',
                message=str(exception),
                debug=traceback.format_exc() if settings.DEBUG else None,
            ),
            status=400,
        )

    if response is not None and hasattr(response, 'data'):
        if hasattr(response.data['detail'], 'code'):
            response.data['debug'] = traceback.format_exc() if settings.DEBUG else None
            response.data['code'] = response.data['detail'].code
            response.data['title'] = exception.payload if hasattr(exception, 'title') else None
            response.data['message'] = response.data['detail']
            response.data['payload'] = exception.payload if hasattr(exception, 'payload') else None
            del response.data['detail']

    return response
