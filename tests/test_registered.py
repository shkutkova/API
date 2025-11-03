import requests

from data.endpoints import Endpoints
from data.generator.generator import Generator
from modules.registered_module import RegisteredModule
from utils.schemas.assertions import Assertions
from utils.schemas.registered_schemas.request_schema import RegisteredRequestSchema
from utils.schemas.registered_schemas.response_schema import TokenResponseSchema
from utils.schemas.validate import Validate
from http import HTTPStatus as status


class TestRegistered:
    generator = Generator()
    module = RegisteredModule()
    endpoint = Endpoints()
    validate = Validate()
    assertion = Assertions()

    def test_registered_v1(self):
        user_info = next(self.generator.registered_data())
        request_boby = self.module.prepare_data(
            schema=RegisteredRequestSchema,
            data=user_info
        )
        response = requests.post(
            url=f'{self.endpoint.base_url}{self.endpoint.api_client}',
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


    def test_registered_v2(self):
        request_boby = self.module.create_request_body(
            schema=RegisteredRequestSchema,
            data_class_instance=next(self.generator.registered_data())
        )
        response = requests.post(
            url=f'{self.endpoint.base_url}{self.endpoint.api_client}',
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