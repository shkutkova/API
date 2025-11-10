from utils.schemas.logger import log    # Здесь импортируется декоратор @log


class BaseModule:       #Это базовый (родительский) класс — как фундамент, на котором строятся другие модули.
# Он не делает конкретных запросов, но умеет:
# Создавать JSON-тело запроса (create_request_body)
# Создавать URL-адрес (create_url)
    @log
    def create_request_body(self, schema, data_class_instance): # Он создаёт JSON-тело запроса из экземпляра дата-класса (объекта с атрибутами данных).
        # Шаг 1: получить все данные из объекта data_class_instance.__dict__
        # Шаг 2: собрать их в словарь
        data_dict = {
            key: value for key, value in data_class_instance.__dict__.items()
        }
        # Шаг 3: создать экземпляр схемы schema(**data_dict)
        # schema здесь — это Pydantic-модель, которая проверяет структуру данных.
        return schema(**data_dict).model_dump_json(by_alias=True)
        # Шаг 4: превратить в JSON model_dump_json
        # by_alias=True — если в схеме есть алиасы полей (например, userName вместо name), то они тоже применяются.

    @log
    def create_url(self, func, endpoint, **kwargs) -> str:
        return func(endpoint, **kwargs)
# '''Как это работает:
# func — это функция, которую ты передаёшь (например, твоя фикстура create_endpoint)
# endpoint — часть пути (например, "users")
# **kwargs — параметры запроса (например, page=2)'''
#
# '''Пример:
# url = base_module.create_url(create_endpoint, "users", page=2)
# Вызовет внутри:
# create_endpoint("users", page=2)
# И вернёт:
# https://reqres.in/api/users?page=2'''