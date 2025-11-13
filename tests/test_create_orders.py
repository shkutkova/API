import requests
from data.endpoints import Endpoints
from data.generator.generator import Generator
from modules.registered_module import RegisteredModule
from utils.schemas.assertions import Assertions
from utils.schemas.create_orders.request_schema import CreateOrdersRequestSchema
from utils.schemas.validate import Validate
from http import HTTPStatus as status


class TestCreateOrders:
    generator = Generator()
    module = RegisteredModule()
    endpoint = Endpoints()
    validate = Validate()
    assertion = Assertions()

    def test_create_orders(self, create_endpoint, get_auth_token):
        user_info = next(self.generator.create_orders_date())
        request_body = self.module.create_orders_date(
            schema=CreateOrdersRequestSchema,
            data=user_info
        )
        print(f"User info: {user_info}")
        print(f"Request body: {request_body}")
        
        response = requests.post(
            url=f'{self.endpoint.base_url}/{self.endpoint.ordersrde}',
            data=request_body
        )
        self.validate.validate(response, CreateOrdersRequestSchema)
        self.assertion.assert_status_code(response,status.CREATED)