# from dataclasses import Field

import requests
from pydantic import BaseModel, Field
# BaseModel - мощная библиотека для валидации данных.
# Она проверяет, что ответ от сервера (JSON) совпадает с нужной структурой и типами.


class UserRegisteredSchema(BaseModel): # Это модель(схема), описывающая какие поля ожидаются при регистрации клиента.
    client_name: str = Field(..., alias='clientName')
    client_email: str = Field(..., alias='clientEmail')


class TokenResponseSchema(BaseModel): # А это схема(модель) ответа сервера, если регистрация прошла успешно.
    access_token: str = Field(..., alias='accessToken')


# def test1():
#     url = "https://simple-books-api.click/api-clients"
#     data = {
#             "clientName": "Pofjffjahj8812",
#             "clientEmail": "gfgfdjdjle978in@example.com"
#     }
#     response = requests.post(url, json=data)
#     print(response.json())


def test2():
    url = "https://simple-books-api.click/api-clients"
    data = {
            "clientName": "Pofrpppppppp7l912",
            "clientEmail": "gftr8ffdgh6pppppp6@example.com"
    }
    response = requests.post(url, json=data)    # Получаем ответ - тело ответа в формате Python-словаря.
    try:
        TokenResponseSchema.model_validate(response.json())     # передаем ответ в схему
                                            # Если JSON совпадает с ожидаемой структурой - все ок
    except ValueError as e:                    # Если не совпадает - выводим ошибку
        raise ValueError("неверный формат тела ответа")