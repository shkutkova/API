from utils.schemas.logger import log


class BaseModule:    # Он может Создавать JSON-тело запроса (create_request_body), URL-адрес (create_url)
    @log
    def create_request_body(self, schema, data_class_instance):# Получить данные из объекта data_class_instance.__dict__
        data_dict = {           # Собираем их в словарь
            key: value for key, value in data_class_instance.__dict__.items()   # __dict__ - это атрибут Python - превращает данные в словарь 
        }
        # Создаем экземпляр схемы schema(**data_dict)
        return schema(**data_dict).model_dump_json(by_alias=True)   # превратить в JSON model_dump_json

    @log
    def create_url(self, func, endpoint, **kwargs) -> str:
        return func(endpoint, **kwargs)
    
# Как это работает:
# func — это функция, которую ты передаёшь (например, твоя фикстура create_endpoint)
# endpoint — часть пути (например, "users")
# **kwargs — параметры запроса (например, page=2)
#
# Пример:
# url = base_module.create_url(create_endpoint, "users", page=2)
# Вызовет внутри:
# create_endpoint("users", page=2)
# И вернёт:
# https://reqres.in/api/users?page=2