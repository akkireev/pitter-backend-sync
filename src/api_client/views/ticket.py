from typing import Dict
from uuid import uuid4

from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from api_client.validation_serializers import TicketPostRequest
from api_client.validation_serializers import TicketPostResponse
from pitter import exceptions
from pitter.decorators import request_post_serializer, response_dict_serializer

from pitter.models.ticket import Ticket


class TicketMobileView(APIView):
    @classmethod
    @request_post_serializer(TicketPostRequest)
    @response_dict_serializer(TicketPostResponse)
    @swagger_auto_schema(
        tags=['Pitter: mobile'],
        request_body=TicketPostRequest,
        responses={
            200: TicketPostResponse,
            401: exceptions.ExceptionResponse,
            404: exceptions.ExceptionResponse,
            500: exceptions.ExceptionResponse,
        },
        operation_summary='Создание заявки',
        operation_description='Создание заявки в сервисе Pitter',
    )
    def post(cls, request) -> Dict[str, str]:
        """
        Создание заявки клиентом
        :param request:
        :return:
        """

        message: str = request.data['message']
        user_comment: str = request.data['userComment']
        fake_id: str = str(uuid4())

        result = Ticket.create_ticket(
            fake_id=fake_id,
            message=message,
            user_comment=user_comment,
        )

        return result.to_dict()
