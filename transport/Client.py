class Client: # определяем класс Client, который представляет клиента компании
    def __init__(self, name, cargo_weight, is_vip=False): # конструктор класса, принимающий имя, вес груза и VIP-статус (по умолчанию False)
        if not name or not name.strip():
            raise ValueError("Имя клиента не может быть пустой строкой.")
        
        if not isinstance(cargo_weight, (int, float)) or cargo_weight < 0:
            raise ValueError("Вес груза должен быть положительным числом.")
        
        if not isinstance(is_vip, bool):
            raise ValueError("VIP-статус должен быть True или False.")
        
        self.name = name.strip() # сохраняем имя клиента, убирая лишние пробелы в начале и конце
        self.cargo_weight = cargo_weight # сохраняем вес груза клиента
        self.is_vip = is_vip # сохраняем VIP-статус клиента