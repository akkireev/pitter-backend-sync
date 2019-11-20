import functools

from rest_framework.response import Response

from pitter.exceptions import exceptions


def request_post_serializer(serializer):
    """
    Валидация данных запроса
    :param serializer: serializer instance
    :return:
    """

    def _decorator(handler):
        @functools.wraps(handler)
        def _wrapper(view, request, *args, **kwargs):
            ser = serializer(data=request.data)
            if not ser.is_valid():
                raise exceptions.ValidationError(message=str(ser.errors))
            return handler(view, request, *args, **kwargs)

        return _wrapper

    return _decorator


def request_query_serializer(serializer):
    """
    Валидация данных запроса в query
    :param serializer: serializer instance
    :return:
    """

    def _decorator(handler):
        @functools.wraps(handler)
        def _wrapper(view, request, *args, **kwargs):
            ser = serializer(data=request.query_params)
            if not ser.is_valid():
                raise exceptions.ValidationError(message=str(ser.errors))
            return handler(view, request, *args, **kwargs)

        return _wrapper

    return _decorator


def response_dict_serializer(serializer=None):
    """
    Валидация данных ответа
    :param serializer: serializer instance
    :return:
    """

    def _decorator(handler):
        @functools.wraps(handler)
        def _wrapper(view, request, *args, **kwargs):
            response_data = handler(view, request, *args, **kwargs)
            if not serializer:
                return Response(response_data)
            ser = serializer(data=response_data)
            if not ser.is_valid():
                raise exceptions.ValidationError(message=str(ser.errors))
            return Response(ser.validated_data)

        return _wrapper

    return _decorator


def response_list_serializer(serializer=None):
    """
    Валидация данных ответа
    :param serializer: serializer instance
    :return:
    """

    def _decorator(handler):
        @functools.wraps(handler)
        def _wrapper(view, request, *args, **kwargs):
            response_data = handler(view, request, *args, **kwargs)
            if not serializer:
                return Response(response_data)
            ser = serializer(data=response_data, many=True)
            if not ser.is_valid():
                raise exceptions.ValidationError(message=str(ser.errors))
            return Response(ser.validated_data)

        return _wrapper

    return _decorator
