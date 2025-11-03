from dataclasses import dataclass   '''удобный способ описывать “структуру данных” 
                            без лишнего кода (примерно как мини-класс с автогенерацией __init__).'''
import requests         # отправляем HTTP-запросы.
from faker import Faker # библиотека, которая создаёт случайные, реалистичные данные
from pydantic import BaseModel, Field     # BaseModel - для описания и валидации структуры данных
                                # Field - преобразование Python-имен (client_name) в JSON-ключи (clientName).

fake = Faker()  # Создаётся объект fake, с помощью него генерируются случайные данные.


@dataclass      # декоратор который автоматически создаёт “вспомогательный” код для класса
'''Python сам генерирует для этого класса:
метод __init__ (конструктор),
метод __repr__ (удобный вывод в консоли),

class Register:
    def __init__(self, client_name=None, client_email=None):
        self.client_name = client_name
        self.client_email = client_email

    def __repr__(self):
        return f"Register(client_name={self.client_name!r}, client_email={self.client_email!r})"

'''
class Register:
    client_name: str = None
    client_email: str = None

def generate_register_user():
    yield Register(                    # yield, то есть функция возвращает генератор.
        client_name=fake.name(),
        client_email=fake.email()
    )

class UserRegistrationSchema(BaseModel):        # Pydantic-схема для API
    client_name: str = Field(..., alias="clientName")       # alias="clientName" — задаёт “псевдоним” для имени поля.
    client_email: str = Field(..., alias="clientEmail")     # Три точки ... — означают, что поле обязательно.


def test1():
    user = next(generate_register_user())       # next() запрашивает у генератора yield первое значение
    print(user.client_name)
    print(user.client_email)

def test2():
    url = "https://simple-books-api.click/api-clients"
    user = next(generate_register_user())       # получаем нового случайного пользователя.
    data = UserRegistrationSchema(
        clientName=user.client_name,             # создаём объект модели Pydantic.
        clientEmail=user.client_email           # Именно clientName и clientEmail.
                                            # Это соответствуют тому, как сервер ожидает данные в JSON.
    )
    data = data.model_dump(by_alias=True)   # превращает модель в словарь, где ключи заменяются на алиасы
    '''model_dump() - Превращает Pydantic-объект в обычный словарь Python.
Если использовать by_alias=True, то ключи словаря будут как в JSON для API, а не как в Python:
data.model_dump(by_alias=True)
# -> {'clientName': 'Anna Smith', 'clientEmail': 'anna@example.com'}
'''
    response = requests.post(url, json=data)
    print(response.json())
    print(response.status_code)