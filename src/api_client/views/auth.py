from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import RegistrationPostRequest
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer
from pitter.exceptions import AlreadyExistsError
from pitter.models import User


class RegistrationMobileView(APIView):
    @classmethod
    @request_post_serializer(RegistrationPostRequest)
    @response_dict_serializer()
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=RegistrationPostRequest,
        responses={
            201: None,
            400: exceptions.ExceptionResponse,
            401: exceptions.ExceptionResponse,
            409: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Создание учетной записи',
        operation_description='Создание учетной записи в сервисе Pitter',
    )
    def post(cls, request) -> None:
        """
        Создание учетной записи клиентом
        :param request:
        :return:
        """
        login: str = request.data['login']
        password: str = request.data['password']

        user, registered = User.register_new_user(
            login=login,
            password=password
        )

        if registered:
            return None
        else:
            raise AlreadyExistsError(message="Пользователь с таким логином уже существует", status_code=409)
