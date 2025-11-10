from http.client import responses
from pprint import pprint

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

    def test_registered_v1(self, request_body=None):    # (self, create_endpoint):
        user_info = next(self.generator.registered_data()) # request_body = self.module.create_request_body(
        request_body = self.module.prepare_data(            # schema=RegisteredRequestSchema,
            schema=RegisteredRequestSchema,                 # data_class_instance=next(self.generator.registered_data())
            data=user_info                                  # )
        )
        response = requests.post(
            url=f'{self.endpoint.base_url}/{self.endpoint.api_client}',
            #  url=f'{self.module.create_url(create_endpoint, self.endpoint.api_client)}',
            data=request_body,
        )
        self.validate.validate(
            response=response,
            schema=TokenResponseSchema,
        )
        self.assertion.assert_status_code(
            response=response,
            status_code=status.CREATED
        )

    def test_user_registered(self, registered_user):
        assert "token" in registered_user
        assert registered_user["token"] is not None
        token = registered_user["token"]
        print(token)

    def test_get_orders(registered_user):
        token = registered_user["token"]
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(f'{Endpoints().base_url}/orders', headers=headers)
        assert response.status_code == 200

    def test_get_status(self):
        response = requests.get(
            url=f'{self.endpoint.base_url}/{self.endpoint.status}'
        )
        self.assertion.assert_status_code(
            response=response,
            status_code=200
        )

    def test_list_of_books(self, create_endpoint):
        response = requests.get(
            url=f'{self.module.create_url(create_endpoint, self.endpoint.books)}'
        )
        self.assertion.assert_status_code(
            response=response,
            status_code=200
        )
        print(response.json())

    def test_get_a_single_book(self):
        response = requests.get(
            url=f'{self.endpoint.base_url}/{self.endpoint.books}/{self.endpoint.id}'
        )
        self.assertion.assert_status_code(
            response=response,
            status_code=200
        )
        pprint(response.json())

    def test_get_all_orders(self):
        response = requests.get(
            url=f'{self.endpoint.base_url}/{self.endpoint.orders}'
        )
        self.assertion.assert_status_code(
            response=response,
            status_code=200
        )
        print(response.json())

