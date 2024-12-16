from .Vehicle import Vehicle

class Truck(Vehicle):
    _id_counter = 1  # Счетчик для уникальных ID
    def __init__(self, capacity, color):
        super().__init__(capacity)
        if not isinstance(color, str) or not color.strip(): # проверка на всякий бред по типу пробела вместо строки
            raise ValueError("Цвет должен быть непустой строкой.")
        
        self.id = Truck._id_counter
        Truck._id_counter += 1
        self.color = color  # цвет грузовика

    def __str__(self):
        first_str = super().__str__() # получаем изначальную строку
        return f"Грузовик, {first_str}, Цвет: {self.color}" # добавляем цвет в строку