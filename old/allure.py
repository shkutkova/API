import requests
import allure       # библиотека для красивых отчётов по тестам
from log import log

@allure.epic('Test allure')     # верхний уровень группировки в Allure.
class TestAllure:

    @log
    @allure.feature('Get all books')        # функциональная группа в Allure
    @allure.description('Тест проверяет получение списка всех книг')    # описание теста, будет отображаться в отчёте.
    @allure.severity(allure.severity_level.CRITICAL)    # указывает важность теста. CRITICAL = критический.
    def test_get_books2(self):
        with allure.step('Получение урла'):         # создаёт шаг в отчёте Allure.
            url = "https://simple-books-api.click/books"
        with allure.step('Отправка запроса'):       # Шаг для отправки GET-запроса.
            response = requests.get(url)
        with allure.step('Получение статус кода и сравнение его с 200'):
            assert response.status_code == 200, f"Неверный статус код. Ожидали 200, получили {response.status_code}"