from pydantic import BaseModel


class CreateOrdersRequestSchema(BaseModel):
    bookId: int
    customerName: str