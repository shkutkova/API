from pydantic import ValidationError

from utils.schemas.logger import log


class Validate:

    @log
    def validate(self, response, schema):
        """
        Валидирует тело ответа на основании переданной схемы
        """
        try:
            schema.model_validate(response.json())
        except ValidationError as e:
            return ValueError(f"Invalid response : {e}")