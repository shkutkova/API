
from modules.base_module import BaseModule
from utils.schemas.logger import log


class RegisteredModule(BaseModule):     # класс-наследник от BaseModule

    @log
    # Подготавливаем данные для запроса на основе схемы
    def prepare_data(self, schema, data):   # создаёт тело для API-запроса регистрации,
                            # используя схему Pydantic (schema) и объект с данными (data).
        # Шаг 1. Вызов схемы
        prepare_data = schema(      # Здесь создаётся экземпляр схемы
            clientName=data.clientName,
            clientEmail=data.clientEmail
        ).model_dump_json(by_alias=True)    # Шаг 2. Превращение в JSON
        return prepare_data
