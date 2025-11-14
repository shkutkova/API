import requests
from data.endpoints import Endpoints
from data.generator.generator import Generator
from modules.create_order_module import CreateOrderModule
from modules.registered_module import RegisteredModule
from utils.schemas.assertions import Assertions
from utils.schemas.create_orders.request_schema import CreateOrdersRequestSchema
from utils.schemas.create_orders.respond_schema import CreateOrdersRespondSchema, OneOrderRespondSchema
from utils.schemas.validate import Validate
from http import HTTPStatus as status


class TestCreateOrders:
    generator = Generator()
    module = CreateOrderModule()
    endpoint = Endpoints()
    validate = Validate()
    assertion = Assertions()

    # def test_create_orders(self, create_endpoint, get_auth_token):
    #     user_info = next(self.generator.create_orders_date())
    #     request_body = self.module.create_order(
    #         schema=CreateOrdersRequestSchema,
    #         data=user_info
    #     )
    #     print(f"User info: {user_info}")
    #     print(f"Request body: {request_body}")
    #     response = requests.post(
    #         url=f'{self.endpoint.base_url}/{self.endpoint.orders}',
    #         headers=get_auth_token,
    #         data=request_body
    #     )
    #     self.validate.validate(response, CreateOrdersRespondSchema)
    #     self.assertion.assert_status_code(response,status.CREATED)

    def test_create_order(self, create_order):
        print(f"User info: {create_order}")
        assert create_order["order_id"] is not None

    def test_get_all_orders(self, create_endpoint, get_auth_token, create_order):
        response = requests.get(
            url=f'{self.endpoint.base_url}/{self.endpoint.orders}',
            headers=get_auth_token
        )
        orders = response.json()
        self.assertion.assert_status_code(      # Проверка status code
            response=response,
            status_code=status.OK)
        assert any(o["id"] == create_order["order_id"] for o in orders)



    def test_get_an_order(self, create_endpoint, get_auth_token, create_order):
        response = requests.get(
            url=f'{self.endpoint.base_url}/{self.endpoint.orders}/{create_order["order_id"]}',
            headers=get_auth_token,
        )
        order_data = OneOrderRespondSchema(**response.json())
        assert order_data.id == create_order["order_id"]
        self.assertion.assert_status_code(  # Проверка status code
            response=response,
            status_code=status.OK)