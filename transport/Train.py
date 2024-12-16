from .Vehicle import Vehicle # импортируем класс Vehicle из модуля Vehicle, который находится в том же пакете

class Train(Vehicle): # определяем класс Train, который наследует от класса Vehicle
    _id_counter = 1  # Счетчик для уникальных ID
    def __init__(self, capacity, number_of_cars): # конструктор класса Train, принимающий грузоподъемность и количество вагонов
        super().__init__(capacity) # вызываем конструктор родительского класса Vehicle для инициализации грузоподъемности
        if not isinstance(number_of_cars, int) or number_of_cars <= 0:
            raise ValueError("Количество вагонов должно быть положительным целым числом.")
        self.number_of_cars = number_of_cars # сохраняем количество вагонов поезда
        self.id = Train._id_counter
        Train._id_counter += 1

    def __str__(self): # метод для строкового представления объекта Train
        first_str = super().__str__() # получаем строковое представление родительского класса Vehicle
        return f"Поезд, {first_str}, Количество вагонов: {self.number_of_cars}"