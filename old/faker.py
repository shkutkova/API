from dataclasses import dataclass       # удобный способ описывать “структуру данных”
import requests 
from faker import Faker 
from pydantic import BaseModel, Field     

fake = Faker()  # Создаётся объект fake, с помощью него генерируются случайные данные.


@dataclass      # декоратор который автоматически создаёт “вспомогательный” код для класса

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
    client_email: str = Field(..., alias="clientEmail")     # Три точки ... — поле обязательно.


def test1():
    user = next(generate_register_user())       # next() запрашивает у генератора yield первое значение
    print(user.client_name)
    print(user.client_email)


def test2():
    url = "https://simple-books-api.click/api-clients"
    user = next(generate_register_user())       # получаем нового случайного пользователя.
    data = UserRegistrationSchema(
        clientName=user.client_name,            # Именно clientName и clientEmail. 
        clientEmail=user.client_email           # (Это соответствуют тому, как сервер ожидает данные в JSON)                                        
    )
    data = data.model_dump(by_alias=True)   # model_dump() - Превращает Pydantic-объект в словарь Python.
                            # by_alias=True, то ключи словаря будут как в JSON для API, а не как в Python:
    response = requests.post(url, json=data)
    print(response.json())
    print(response.status_code)