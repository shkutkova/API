from modules.base_module import BaseModule
from utils.schemas.create_orders.request_schema import CreateOrdersRequestSchema


class CreateOrderModule(BaseModule):
    # pass
    def create_order(self, schema, data):
        create_order = schema(
            bookId=data.bookId,
            customerName=data.customerName
        ).model_dump_json(by_alias=True)
        return create_order
