from pydantic import BaseModel


class CreateOrdersRespondSchema(BaseModel):
    created: bool
    orderId: str

class OneOrderRespondSchema(BaseModel):
    id: str
    bookId: int
    customerName: str
    quantity: int
    timestamp: int