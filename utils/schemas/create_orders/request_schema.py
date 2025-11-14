from pydantic import BaseModel, Field



class CreateOrdersRequestSchema(BaseModel):
    bookId: int = Field(ge=3, le=5)
    customerName: str


# class CreateOrderRequestSchema(BaseModel):
#     book_id: int = Field(..., alias="bookId")
#     customer_name: str = Field(..., alias="customerName")