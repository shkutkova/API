from utils.schemas.logger import log


class Assertions:   # этот класс отвечает за проверки (assert’ы) в тестах, то есть за валидацию результатов запросов.

    @log
    # Шаг 1. Аргументы: response — это ответ от сервера, полученный после запроса.
    # Например, результат requests.get() или requests.post(). status_code — ожидаемый HTTP (например, 200, 201, 404)
    def assert_status_code(self, response, status_code):
        assert response.status_code == status_code, \
            f'Неверный статус код. Ожидали {status_code} статус, получили {response.status_code} статус '