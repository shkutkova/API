import random
import requests
from http import HTTPStatus
import allure
import pytest

from faker import Faker

from data.endpoints import Endpoints
from data.generator.generator import Generator
from modules.create_order_module import CreateOrderModule
from utils.schemas.assertions import Assertions
from utils.schemas.create_orders.request_schema import CreateOrderRequestSchema
from utils.schemas.create_orders.respond_schema import CreateOrdersRespondSchema
from utils.schemas.validate import Validate

fake = Faker()

@pytest.mark.regression      # маркировка?
class TestOrder:
    generator = Generator()
    module = CreateOrderModule()
    endpoint = Endpoints()
    validate = Validate()
    assertion = Assertions()

    @allure.title("Создание заказа")
    def test_create_order(self, auth_order_client: OrderClient, book_client: BooksClient):
        get_books_response =  book_client.get_books()
        random_book_id = random.choice(get_books_response).id

        print(f"book id = {random_book_id}")
        request = CreateOrderRequestSchema(
            book_id=random_book_id,
            customer_name=fake.name()
        )
        response = auth_order_client.create_order_api(request=request)
        print(f"response = {response.json()}")
        response_data = CreateOrderResponseSchema.model_validate_json(response.text)

        assert HTTPStatus.CREATED == response.status_code

    # @pytest.mark.skip
    @allure.title("Получение созданного заказа")
    def test_get_order(self, order_client: OrderClient, order: OrderFixture):
        response = order_client.get_order_by_id_api(order_id=order.order_id)
        print(f"заказ - {response.json()}")
        response_data = GetOrderResponseSchema.model_validate_json(response.text)

        assert HTTPStatus.OK == response.status_code
        assert order.order_id == response_data.id

    @allure.title("Изменение заказа")
    def test_update_order(self, order_client: OrderClient, order: OrderFixture):
        response = order_client.get_order_by_id_api(order_id=order.order_id)
        response_data = GetOrderResponseSchema.model_validate_json(response.text)
        assert order.order_id == response_data.id

        update_request = UpdateOrderRequestSchema(
            customer_name=fake.name()
        )
        update_response = order_client.update_order_api(order_id=order.order_id, request=update_request)
        assert HTTPStatus.NO_CONTENT == update_response.status_code

        get_response = order_client.get_order_by_id_api(order_id=order.order_id)
        get_response_data = GetOrderResponseSchema.model_validate_json(get_response.text)

        assert order.request.customer_name != get_response_data.customer_name
        assert update_request.customer_name == update_request.customer_name

    @allure.title("Удаление заказа")
    def test_delete_order(self, order_client: OrderClient, order: OrderFixture):
        response = order_client.delete_order_api(order_id=order.order_id)
        assert HTTPStatus.NO_CONTENT == response.status_code

        get_response = order_client.get_order_by_id_api(order_id=order.order_id)
        assert HTTPStatus.NOT_FOUND == get_response.status_code