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
        user_info = next(self.generator.registered_data())
        request_body = self.module.prepare_data(
            schema=RegisteredRequestSchema,     # импортируем схему запроса (name, email)
            data=user_info
        )
        print(f"User info: {user_info}")
        print(f"Request body: {request_body}")
        
        response = requests.post(       # Отправляем post запрос
            url=f'{self.endpoint.base_url}/{self.endpoint.api_client}',     # < на этот URL
            data=request_body,          # с телом request_body /\
        )
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        self.validate.validate(         # Валидация JSON-ответа
            response=response,
            schema=TokenResponseSchema,     # есть ли поле token в ответе по схеме TokenResponseSchema
        )
        self.assertion.assert_status_code(      # Проверка status code
            response=response,
            status_code=status.CREATED
        )


    def test_registered_v2(self):
        request_body = self.module.create_request_body(
            schema=RegisteredRequestSchema,
            data_class_instance=next(self.generator.registered_data())
        )
        print(f"Request body: {request_body}")
        response = requests.post(
            url=f'{self.endpoint.base_url}/{self.endpoint.api_client}',
            data=request_body,
        )
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
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