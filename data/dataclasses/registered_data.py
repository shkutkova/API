from dataclasses import dataclass
# dataclass — декоратор, который позволяет быстро создавать классы для хранения данных

@dataclass()
class RegisteredDataClass:
    clientName: str = None
    clientEmail: str = None
