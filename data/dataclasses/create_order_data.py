from dataclasses import dataclass

@dataclass
class CreateOrdersDataClass:
    bookId: int = None
    customerName: str = None