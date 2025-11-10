from dataclasses import dataclass
# '''dataclass — это специальный декоратор из стандартной библиотеки Python,
# который позволяет быстро создавать классы для хранения данных
# Он автоматически добавляет:
# __init__ (конструктор)
# __repr__ (удобное отображение в консоли)
# __eq__ (сравнение объектов)'''
@dataclass()
class RegisteredDataClass:
    clientName: str = None
    clientEmail: str = None
