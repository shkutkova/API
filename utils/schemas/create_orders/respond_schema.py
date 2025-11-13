from pydantic import BaseModel


class CreateOrderdRespondSchema(BaseModel):
    created: bool
    orderId: str