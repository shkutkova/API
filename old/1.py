from pprint import pprint

import requests     # requests — библиотека, с помощью которой Python отправляет HTTP-запросы (GET, POST и т.д.).

def test_get_books():
    url = "https://simple-books-api.click/books"
    response = requests.get(url)
    print(response)         # объект с ответом от сервера.
    pprint(response.json())     # превращает ответ в Python-словарь
    print(response.status_code)
    print(response.url)

def test_get_books1():
    url = "https://simple-books-api.click/books"
    response = requests.get(url)
    assert response.status_code == 200  # assert — это встроенная проверка в Python
                                        # Проверяет (через assert), что код ответа равен 200.


def test_get_books2():
    url = "https://simple-books-api.click/books"
    response = requests.get(url)
    assert response.status_code == 200, f"Неверный статус код. Ожидали 200, получили {response.status_code}"