import os                           # модуль для работы с переменными окружения и путями
from urllib.parse import urlencode
# превращает словарь параметров в строку param1=value1&param2=value2,
# которая добавляется в URL после знака ?
import pytest           # нужен, чтобы объявить фикстуру (через @pytest.fixture)
import requests
from dotenv import load_dotenv

from data.endpoints import Endpoints
from data.generator.generator import Generator
from modules.registered_module import RegisteredModule
from utils.schemas.registered_schemas.request_schema import RegisteredRequestSchema

load_dotenv()       # находит файл .env в корне проекта и подгружает все пары KEY=VALUE в системные переменные окружения.

BASE_URL = os.getenv('BASE_URL')    # достаёт значение переменной BASE_URL (например, https://reqres.in/api).

@pytest.fixture         # ф-ция создает нам данные
def create_endpoint():
# Эта строка говорит pytest: «Вот функция, которую можно использовать как фикстуру».
# Она не возвращает данные напрямую, а создаёт внутреннюю функцию _build_endpoint, и возвращает именно её.

    def _build_endpoint(path: str, **kwargs):
        url = f'{BASE_URL}/{path}'      # Шаг 1: создание базового пути
        params = {key: value for key, value in kwargs.items() if value is not None}  # Шаг 2: обработка параметров запроса
            # '''**kwargs — это все дополнительные аргументы, переданные в функцию.
            # Например: _build_endpoint("users", page=2, per_page=5) → kwargs = {'page': 2, 'per_page': 5}
            # Команда фильтрует их, удаляя те, где значение None.'''
        return f'{url}?{urlencode(params,doseq=True)}' if params else url
            # Если параметры есть → добавляем их к URL через ?. urlencode(params)
            # превратит {'page': 2, 'per_page': 5} в строку page = 2 & per_page = 5.
    return _build_endpoint

@pytest.fixture(scope="session")
def registered_user():
    module = RegisteredModule()
    generator = Generator()
    endpoint = Endpoints()

    user_info = next(generator.registered_data())
    request_body = module.prepare_data(schema=RegisteredRequestSchema, data=user_info)
    response = requests.post(f'{endpoint.base_url}/{endpoint.api_client}', data=request_body)

    assert response.status_code == 201, f"Ошибка регистрации: {response.text}"
    token = response.json()['accessToken']

    return {"token": token, "user": user_info}
