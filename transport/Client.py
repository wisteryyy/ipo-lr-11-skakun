class Client: # определяем класс Client, который представляет клиента компании
    def __init__(self, name, cargo_weight, is_vip=False): # конструктор класса, принимающий имя, вес груза и VIP-статус (по умолчанию False)
        if not name.isalpha() or len(name) < 2: # проверяем, что имя состоит только из букв и длина не менее 2
            raise ValueError("Имя клиента должно содержать только буквы и быть не менее 2 символов.")

        if not isinstance(cargo_weight, (float, int)) or cargo_weight <= 0 or cargo_weight > 10000: # проверяем, что вес положительный и не превышает 10000
            raise ValueError("Вес груза должен быть положительным числом и не более 10000 кг.")

        if not isinstance(is_vip, bool):
            raise ValueError("VIP-статус должен быть True или False.")
        
        self.name = name.strip() # сохраняем имя клиента, убирая лишние пробелы в начале и конце
        self.cargo_weight = cargo_weight # сохраняем вес груза клиента
        self.is_vip = is_vip # сохраняем VIP-статус клиента

    def to_dict(self): # метод для преобразования объекта клиента в словарь
        return { # возвращаем словарь с данными клиента
            'name': self.name,
            'cargo_weight': self.cargo_weight,
            'is_vip': self.is_vip
        }
