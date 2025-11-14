import os                           # модуль для работы с переменными окружения и путями
from urllib.parse import urlencode  # превращает словарь параметров в строку param1=value1&param2=value2,
                                    # которая добавляется в URL после знака ?
import pytest           # нужен, чтобы объявить фикстуру (через @pytest.fixture)
import requests
from dotenv import load_dotenv

from data.endpoints import Endpoints
from data.generator.generator import Generator
from modules.registered_module import RegisteredModule
from modules.create_order_module import CreateOrderModule
from utils.schemas.create_orders.request_schema import CreateOrdersRequestSchema
from utils.schemas.registered_schemas.request_schema import RegisteredRequestSchema

load_dotenv()       # Загружает переменные из .env файла (KEY=VALUE)

BASE_URL = os.getenv('BASE_URL')    # get из файла .env
generator = Generator()
module = RegisteredModule()
endpoint = Endpoints()
order_module = CreateOrderModule()


@pytest.fixture         # ф-ция создает нам данные
def create_endpoint():

    def _build_endpoint(path: str, **kwargs):
        url = f'{BASE_URL}/{path}'      # Cоздание базового пути
            
            # Фильтруем параметры (убираем None)
        params = {key: value for key, value in kwargs.items() if value is not None}

            # Если параметры есть → добавляем их к URL через ?. urlencode(params)
            # превратит {'page': 2, 'per_page': 5} в строку page = 2 & per_page = 5
        return f'{url}?{urlencode(params,doseq=True)}' if params else url   # urlencode() - превращает словарь в строку параметров
            # doseq - Разбить список на несколько параметров (doseq=True)
            # doseq - Или передать список как одну строку (doseq=False)

    return _build_endpoint



@pytest.fixture(scope='session')
def get_auth_token():
    user_info = next(generator.registered_data())
    request_body = module.prepare_data(
        schema=RegisteredRequestSchema, 
        data=user_info
    )
    response = requests.post(       
            url=f'{endpoint.base_url}/{endpoint.api_client}',
            data=request_body
        )
    token = response.json()['accessToken']

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    return headers

@pytest.fixture
def create_order(get_auth_token):

    # Генерируем данные для заказа
    order_data = next(generator.create_orders_date())
    request_body = order_module.create_order(
        schema=CreateOrdersRequestSchema,
        data=order_data
    )

    # Создаём заказ
    response = requests.post(
        url=f"{endpoint.base_url}/{endpoint.orders}",
        headers=get_auth_token,
        data=request_body
    )
    assert response.status_code == 201, "Не удалось создать заказ"

    order_id = response.json()["orderId"]
    print(order_id)

    # Возвращаем И order_id, И данные (полезно для проверки)
    return {
        "order_id": order_id,
        "order_data": order_data
    }

# @pytest.fixture(scope="session")
# def registered_user():
#      # Инициализация компонентов
#     module = RegisteredModule()     # Для подготовки данных
#     generator = Generator()         # Генератор тестовых данных
#     endpoint = Endpoints()          # Эндпоинты API

#     # Генерация данных пользователя
#     user_info = next(generator.registered_data())
    
#     # Подготовка тела запроса
#     request_body = module.prepare_data(schema=RegisteredRequestSchema, data=user_info)
    
#     # Отправка запроса на регистрацию
#     response = requests.post(f'{endpoint.base_url}/{endpoint.api_client}', data=request_body)

#     # Проверка успешности регистрации
#     assert response.status_code == 201, f"Ошибка регистрации: {response.text}"
    
#     # Извлечение токена из ответа
#     token = response.json()['accessToken']

#     # Возврат данных для использования в тестах
#     return {"token": token, "user": user_info}
