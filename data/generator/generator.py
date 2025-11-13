from faker import Faker
from data.dataclasses.create_order_data import CreateOrdersDataClass
from data.dataclasses.registered_data import RegisteredDataClass


class Generator:
    fake = Faker()

    def registered_data(self):          # генерирует данные для регистрации
        yield RegisteredDataClass(
            clientName=self.fake.name(),
            clientEmail=self.fake.email()
        )


    def create_orders_date(self):
        yield CreateOrdersDataClass(
            bookId=self.fake.random_int(min=3, max=5),
            customerName=self.fake.name()
        )