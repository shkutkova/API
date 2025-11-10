import requests

from data.endpoints import Endpoints
from data.generator.generator import Generator
from modules.registered_module import RegisteredModule
from utils.schemas.assertions import Assertions
from utils.schemas.registered_schemas.request_schema import RegisteredRequestSchema
from utils.schemas.registered_schemas.response_schema import TokenResponseSchema
from utils.schemas.validate import Validate
from http import HTTPStatus as status
# from test import ctx


class TestRegistered:           # экземпляры всех вспомогательных классов
    generator = Generator()
    module = RegisteredModule()
    endpoint = Endpoints()
    validate = Validate()
    assertion = Assertions()

    def test_registered_v1(self, request_body=None):
        user_info = next(self.generator.registered_data()) # registered_data() — генератор, который выдаёт объект RegisteredDataClass.
        request_body = self.module.prepare_data(
            schema=RegisteredRequestSchema,
            data=user_info
        )
        # Шаг 3 Отправка POST-запроса
        # Формируется URL из базового адреса и пути (/api_client)
        # Отправляется запрос с телом request_body
        response = requests.post(
            url=f'{self.endpoint.base_url}/{self.endpoint.api_client}',
            data=request_body,
        )
        # Шаг 4 Валидация JSON-ответа
        # Проверяет, соответствует ли ответ API схеме TokenResponseSchema (есть ли поле token в ответе)
        self.validate.validate(
            response=response,
            schema=TokenResponseSchema,
        )
        # Шаг 5 Проверка status code
        self.assertion.assert_status_code(
            response=response,
            status_code=status.CREATED
        )


    def test_registered_v2(self):
        request_boby = self.module.create_request_body(
            schema=RegisteredRequestSchema,
            data_class_instance=next(self.generator.registered_data())
        )
        response = requests.post(
            url=f'{self.endpoint.base_url}/{self.endpoint.api_client}',
            data=request_boby,
        )
        self.validate.validate(
            response=response,
            schema=TokenResponseSchema,
        )
        self.assertion.assert_status_code(
            response=response,
            status_code=status.CREATED
        )


    def test_registered_v3(self, create_endpoint):
        request_boby = self.module.create_request_body(
            schema=RegisteredRequestSchema,
            data_class_instance=next(self.generator.registered_data())
        )
        response = requests.post(
            url=f'{self.module.create_url(create_endpoint, self.endpoint.api_client)}',
            data=request_boby,
        )
        self.validate.validate(
            response=response,
            schema=TokenResponseSchema,
        )
        self.assertion.assert_status_code(
            response=response,
            status_code=status.CREATED
        )


    # def test_registered_v4(self, create_endpoint):
    #     request_boby = ctx.module.create_request_body(
    #         schema=RegisteredRequestSchema,
    #         data_class_instance=next(ctx.generator.registered_data())
    #     )
    #     response = requests.post(
    #         url=f'{ctx.module.create_url(create_endpoint, self.endpoint.api_client)}',
    #         data=request_boby,
    #     )
    #     ctx.validate.validate(
    #         response=response,
    #         schema=TokenResponseSchema,
    #     )
    #     ctx.assertion.assert_status_code(
    #         response=response,
    #         status_code=status.CREATED
    #     )