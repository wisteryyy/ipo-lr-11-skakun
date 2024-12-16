from .Vehicle import Vehicle # импортируем классы из модулей, которые находятся в том же пакете
from .Client import Client

class TransportCompany: # определяем класс TransportCompany, который представляет транспортную компанию
    def __init__(self, name): # конструктор класса, принимающий название компании
        if not name or not name.strip():
            raise ValueError("Название компании не может быть пустой строкой.")
        self.name = name # сохраняем название компании
        self.vehicles = [] # инициализация пустого списка для транспортных средств
        self.clients = [] # инициализация пустого списка для клиентов

    def add_vehicle(self, vehicle): # метод для добавления транспортного средства в компанию
        if not isinstance(vehicle, Vehicle): # проверяем, что добавляемый объект является экземпляром класса Vehicle
            raise ValueError("Транспортное средство должно быть экземпляром класса Vehicle.")
        self.vehicles.append(vehicle) # добавляем транспортное средство в список

    def list_vehicles(self): # метод для получения списка транспортных средств
        return self.vehicles # возвращаем список транспортных средств

    def add_client(self, client): # метод для добавления клиента в компанию
        if not isinstance(client, Client): # проверяем, что добавляемый объект является экземпляром класса Client
            raise ValueError("Клиентов нет.")
        self.clients.append(client) # добавляем клиента в список

    def list_clients(self): # метод для получения списка клиентов
        return self.clients # возвращаем список клиентов

    def optimize_cargo_distribution(self): # метод для оптимизации распределения грузов
        for vehicle in self.vehicles: # очищаем список загруженных клиентов в каждом транспортном средстве
            vehicle.clients_list.clear()

        vip_clients = [client for client in self.clients if client.is_vip] # получаем список VIP-клиентов
        simple_clients = [client for client in self.clients if not client.is_vip] # получаем список обычных клиентов
        
        vip_clients.sort(key=lambda c: c.cargo_weight, reverse=True) # сортируем VIP-клиентов по весу груза в порядке убывания
        simple_clients.sort(key=lambda c: c.cargo_weight, reverse=True) # сортируем обычных клиентов по весу груза в порядке убывания
        
        for client in vip_clients: # проходим по каждому VIP-клиенту
            for vehicle in self.vehicles: # проходим по каждому транспортному средству
                try:
                    vehicle.load_cargo(client) # загружаем груз в транспортное средство
                    break
                except ValueError: # если возникает ошибка из-за недостатка места
                    continue # переходим к следующему транспортному средству

        for client in simple_clients: # проходим по каждому обычному клиенту
            for vehicle in self.vehicles: # проходим по каждому транспортному средству
                try:
                    vehicle.load_cargo(client) # загружаем груз в транспортное средство
                    break
                except ValueError: # если возникает ошибка из-за недостатка места
                    continue # переходим к следующему транспортному средству

    def __str__(self): # метод для строкового представления объекта TransportCompany
        vehicles_info = ', '.join([str(vehicle) for vehicle in self.vehicles]) # создаем строку с информацией о всех транспортных средствах
        return f"Компания: {self.name}, Транспортные средства: [{vehicles_info}]" # возвращаем строку с названием компании и списком транспортных средств