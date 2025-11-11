from functools import wraps     # вспомогательная функция для декораторов, 
                        #чтобы сохранять имя функции, документацию и сигнатуру оригинальной функции.
import requests
from loguru import logger

logger.remove()     # удаляет стандартный вывод в консоль, чтобы не было дублирования.
logger.add(         # добавляет новый “приёмник логов”:
    sink = r"/Users/katarina/PycharmProjects/API/logs.log",  # файл, куда сохраняем логи.
                                            # r = raw string, берём всё буквально, не обрабатываем \n, \t и т.д.
    level='INFO',
    format='{time} | {level} | {message}',
    rotation="10MB",    # объем файла, новый создаётся, когда текущий достигает 10МБ.
    retention="10 days"     # сколько дней жизни
)

def log(func):      # декоратор, оборачивающий любую функцию.

    @wraps(func)    # сохраняет имя и документацию оригинальной функции
    def wrapper(*args, **kwargs):    # позволяет вызвать исходную функцию с любыми аргументами.
        try:                        # пытаемся вернуть наш тест
            return func(*args, **kwargs)
        except Exception as e:          # если тест падает, то в логи записывается ошибка
            logger.error(f'Error in {func.__name__} : {str(e)}')
            raise
    return wrapper

@log
def test_get_books2():
    url = "https://simple-books-api.click/books"
    response = requests.get(url)
    assert response.status_code == 200, f"Неверный статус код. Ожидали 200, получили {response.status_code}"