import tkinter as tk # импортируем библиотеку tkinter как tk для удобства
import json # импортируем модуль json для работы с JSON-данными
import csv # импортируем модуль csv для работы с CSV-файлами
from tkinter import messagebox, ttk # импортируем messagebox для отображения сообщений и ttk для использования виджетов с темами
from transport.Client import Client # импортируем класс Client из модуля transport.Client
from transport.Truck import Truck # импортируем класс Truck из модуля transport.Truck
from transport.Train import Train # импортируем класс Train из модуля transport.Train
from transport.TransportCompany import TransportCompany # импортируем класс TransportCompany из модуля transport.TransportCompany

class Validator: # создаем класс Validator для проверки данных
    @staticmethod
    def validate_client_data(name: str, cargo_weight: str, is_vip: bool) -> bool: # метод для проверки данных клиента
        if not name.isalpha() or len(name) < 2:
            messagebox.showerror("Ошибка", "Имя клиента должно содержать только буквы и быть не менее 2 символов.")
            return False # возвращаем False, если проверка не пройдена
        
        try: # пробуем выполнить следующий код
            cargo_weight = float(cargo_weight)
            if cargo_weight <= 0 or cargo_weight > 10000:
                messagebox.showerror("Ошибка", "Вес груза должен быть положительным числом и не должен превышать 10000 кг.")
                return False # возвращаем False, если проверка не пройдена
        except ValueError:
            messagebox.showerror("Ошибка", "Вес груза должен быть числом.")
            return False

        if not isinstance(is_vip, bool):
            messagebox.showerror("Ошибка", "VIP-статус должен быть True или False.")
            return False
        return True # если все проверки пройдены, возвращаем True

    @staticmethod
    def validate_vehicle_data(vehicle_type: str, capacity: str, color: str = None, number_of_cars: str = None) -> bool: # метод для проверки данных транспортного средства
        if vehicle_type not in ['Грузовик', 'Поезд']: # проверяем, что тип транспорта правильный
            messagebox.showerror("Ошибка", "Тип транспорта должен быть 'Грузовик' или 'Поезд'.")
            return False
        
        try:
            capacity = float(capacity)
            if capacity <= 0:
                messagebox.showerror("Ошибка", "Грузоподъемность должна быть положительным числом.")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Грузоподъемность должна быть числом.")
            return False
        
        if vehicle_type == 'Грузовик': # если выбран грузовик
            if color is None or color.strip() == "":
                messagebox.showerror("Ошибка", "Цвет не может быть пустым.")
                return False
        if vehicle_type == 'Поезд': # если выбран поезд
            try:
                number_of_cars = int(number_of_cars)
                if number_of_cars <= 0:
                    messagebox.showerror("Ошибка", "Количество вагонов должно быть положительным целым числом.")
                    return False
            except ValueError:
                messagebox.showerror("Ошибка", "Количество вагонов должно быть целым числом.")
                return False
        return True

class TransportCompanyApp: # класс TransportCompanyApp, который представляет приложение транспортной компании
    def __init__(self, root): # метод инициализации класса, принимающий главное окно
        self.root = root # сохраняем ссылку на главное окно
        self.root.title("Транспортная Компания Экспресс") # устанавливаем заголовок окна
        self.root.geometry("820x595") # устанавливаем размеры окна
        self.root.resizable(width=False, height=False) # запрещаем изменение размеров окна
        self.root.configure(bg="white") # устанавливаем белый цвет фона окна

        self.company = TransportCompany("Транспортная Компания") # создаем экземпляр класса TransportCompany
        self.clients_data = self.load_data_from_json_clients() # загружаем данные клиентов из JSON-файла
        self.vehicles_data = self.load_data_from_json_vehicles() # загружаем данные о транспортных средствах из JSON-файла
        self.load_clients() # загружаем клиентов в приложение
        self.load_vehicles() # загружаем транспортные средства в приложение

    def load_data_from_json_clients(self): # метод для загрузки данных клиентов из JSON-файла
        try:
            with open("dump_clients.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError: # если файл не найден
            return [] # возвращаем пустой список

    def load_data_from_json_vehicles(self): # метод для загрузки данных о транспортных средствах из JSON-файла
        try:
            with open("dump_vehicles.json", "r", encoding="utf-8") as file:
                vehicles_data = json.load(file)
                for vehicle_data in vehicles_data: # перебираем каждый словарь с данными транспортного средства
                    if vehicle_data['type'] == 'Грузовик': # если тип "Грузовик"
                        vehicle = Truck(capacity=vehicle_data['capacity'], color=vehicle_data['color']) # создаем объект грузовика
                    elif vehicle_data['type'] == 'Поезд': # если тип "Поезд"
                        vehicle = Train(capacity=vehicle_data['capacity'], number_of_cars=vehicle_data['number_of_cars']) # создаем объект поезда
                    else: # если тип не распознан
                        continue # пропускаем итерацию
                    self.company.add_vehicle(vehicle) # добавляем созданное транспортное средство в компанию
        except FileNotFoundError:
            return []

    def save_data_to_json_clients(self, data): # метод для сохранения данных клиентов в JSON-файл
        data_to_save = [client.to_dict() for client in data] # преобразуем каждый объект клиента в словарь
        with open("dump_clients.json", "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4) # сохраняем данные в файл

    def save_data_to_json_vehicles(self, vehicles_data): # метод для сохранения данных о транспортных средствах в JSON-файл
        vehicles_data_to_save = []  # создаем пустой список для сохранения данных
        for vehicle in vehicles_data: # перебираем все транспортные средства
            if isinstance(vehicle, Truck): # если это грузовик
                vehicles_data_to_save.append({ # добавляем данные о грузовике в список
                    'type': 'Грузовик',
                    'capacity': vehicle.capacity,
                    'color': vehicle.color
                })
            elif isinstance(vehicle, Train): # если это поезд
                vehicles_data_to_save.append({ # добавляем данные о поезде в список
                    'type': 'Поезд',
                    'capacity': vehicle.capacity,
                    'number_of_cars': vehicle.number_of_cars
                })
        with open("dump_vehicles.json", "w", encoding="utf-8") as file:
            json.dump(vehicles_data_to_save, file, indent=4) # сохраняем данные о транспортных средствах в файл

    def load_clients(self): # метод для загрузки клиентов
        if isinstance(self.clients_data, list): # проверяем, что загруженные данные клиентов являются списком
            for client_dict in self.clients_data: # перебираем каждый словарь с данными клиента
                try:
                    client = Client(client_dict['name'], client_dict['cargo_weight'], client_dict['is_vip']) # создаем объект клиента
                    self.company.add_client(client) # добавляем клиента в компанию
                except ValueError as e:
                    print(f"Ошибка при загрузке клиента: {e}")

    def load_vehicles(self): # метод для загрузки транспортных средств
        if isinstance(self.vehicles_data, list):
            for vehicle_dict in self.vehicles_data:
                try:
                    if vehicle_dict['type'] == 'Грузовик':
                        vehicle = Truck(vehicle_dict['capacity'], vehicle_dict['color'])
                    elif vehicle_dict['type'] == 'Поезд':
                        vehicle = Train(vehicle_dict['capacity'], vehicle_dict['number_of_cars'])
                    self.company.add_vehicle(vehicle)
                except ValueError as e:
                    print(f"Ошибка при загрузке транспортного средства: {e}")

        self.setup_ui() # вызываем метод для настройки пользовательского интерфейса

    def setup_ui(self): # метод для настройки пользовательского интерфейса
        frame1 = tk.Frame(self.root, bg='gray15')
        frame1.place(relx=0.25, rely=0.26, relwidth=0.5, relheight=0.5)

        frame2 = tk.Frame(self.root, bg='gray15')
        frame2.place(relx=0.08, rely=0.029, relwidth=0.85, relheight=0.2)

        info_text1 = """
        Добро пожаловать на страничку транспортной
        компании Экспресс!"""
        main_label = tk.Label(self.root, text=info_text1, font=("Arial", 17, 'bold'), fg="white", bg="gray15")
        main_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        info_text2 = """
        Вы можете как просматривать списки уже 
        существующих клиентов, транспортных 
        средств, так и регистрировать их со всеми 
        параметрами. Также наша компания 
        предоставляет возможность распределять 
        груз по транспортным средствам. 

        Чтобы груз клиента распределялся в 
        первоочередном порядке, клиенту нужен 
        VIP-статус."""
        info_label = tk.Label(self.root, text=info_text2, font=("Arial", 12), fg="white", bg="gray15")
        info_label.place(relx=0.487, rely=0.5, anchor=tk.CENTER)

        btn_open_clients = tk.Button(self.root, text="Добавить клиента", width=35, height=5, bg="black", fg="white", command=self.open_new_clientsworkwindow)
        btn_open_clients.place(x=130, y=470)

        btn_open_vehicles = tk.Button(self.root, text="Добавить транспорт", width=35, height=5, bg="black", fg="white", command=self.open_new_vehidesworkwindow)
        btn_open_vehicles.place(x=450, y=470)

        btn_open_cargo = tk.Button(self.root, text="Распределить грузы", width=23, height=5, bg="black", fg="white", command=self.open_new_cargo_distribution)
        btn_open_cargo.pack(side=tk.LEFT, padx=10, pady=10)

        btn_exit = tk.Button(self.root, text="Выйти из программы", width=23, height=5, bg="black", fg="white", command=self.root.quit)
        btn_exit.pack(side=tk.RIGHT, padx=10, pady=10)

        self.status = tk.Label(self.root, text='', bg='white', fg='black') # создаем метку для отображения статуса
        self.status.place(relx=0.5, rely=0.985, anchor=tk.CENTER)

        self.setup_menu() # вызываем метод для настройки меню приложения

    def setup_menu(self): # метод для создания меню приложения
        menubar = tk.Menu(self.root) # создаем объект меню, привязанный к главному окну
        export_menu = tk.Menu(menubar, tearoff=0) # создаем подменю для экспорта, отключая возможность "отрыва" меню
        export_menu.add_command(label="Экспорт результата", command=self.export_results) # добавляем команду для экспорта результатов
        export_menu.add_separator() # добавляем разделитель в меню
        export_menu.add_command(label="О программе", command=self.show_about) # добавляем команду для отображения информации о программе
        menubar.add_cascade(label="Меню", menu=export_menu) # добавляем подменю в главное меню
        self.root.config(menu=menubar) # настраиваем главный экран для использования созданного меню

    def export_results(self): # метод для экспорта результатов распределения грузов в CSV файл
        filename = "cargo_distribution_results.csv" # устанавливаем имя файла для сохранения результатов
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file: # открываем файл для записи, создавая его, если он не существует
                writer = csv.writer(file) # создаем объект writer для записи в CSV файл
                writer.writerow(["Тип транспорта", "Грузоподъемность", "Загруженные клиенты"]) # записываем заголовки столбцов

                for vehicle in self.company.vehicles: # проходим по всем транспортным средствам в компании
                    writer.writerow([type(vehicle).__name__, vehicle.capacity, # записываем тип транспорта, грузоподъемность и список загруженных клиентов
                                     ', '.join([client.name for client in vehicle.clients_list]) if vehicle.clients_list else "Нет загруженных клиентов"])
            
            messagebox.showinfo("Экспорт результата", f"Результаты успешно экспортированы в файл: {filename}") # выводим сообщение об успешном экспорте результатов
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать результаты: {e}")

    def show_about(self): # метод для отображения информации о программе
        messagebox.showinfo("О программе", "Транспортная Компания Экспресс\nЛабораторная работа №12\nВариант 1\nВыполнила: София Скакун (70%) и AI Chat (30%)")

    def open_new_clientsworkwindow(self): # метод для открытия нового окна работы с клиентами
        self.root.withdraw() # скрываем главное окно приложения
        new_window = tk.Toplevel(self.root) # создаем новое верхнее окно
        new_window.title("Действия с клиентами")
        new_window.geometry("820x595")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg="white")

        self.frame = tk.Frame(new_window, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.client_table = ttk.Treeview(self.frame, columns=("Имя", "Вес", "VIP"), show='headings') # создаем таблицу для отображения клиентов с колонками "Имя", "Вес" и "VIP статус"
        self.client_table.heading("Имя", text="Имя клиента") # устанавливаем заголовок для колонки 
        self.client_table.heading("Вес", text="Вес груза")
        self.client_table.heading("VIP", text="VIP статус")
        self.client_table.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        frame3 = tk.Frame(new_window, bg='gray15')
        frame3.place(relx=0.08, rely=0.029, relwidth=0.85, relheight=0.2)

        info_text3 = """
        Какую именно операцию Вы бы хотели 
        совершить?"""
        main_label = tk.Label(new_window, text=info_text3, font=("Arial", 16, 'bold'), fg="white", bg="gray15")
        main_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        btn_add_client = tk.Button(new_window, text="Добавить клиента", width=35, height=3, bg="black", fg="white", command=self.add_client)
        btn_add_client.place(x=150, y=180)

        btn_delete_client = tk.Button(new_window, text="Удалить клиента", width=35, height=3, bg="black", fg="white", command=self.delete_client)
        btn_delete_client.place(x=300, y=250)

        btn_return = tk.Button(new_window, text="Назад", width=35, height=3, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.place(x=450, y=180)

        self.load_clients_to_table() # загружаем данные о клиентах в таблицу

    def load_clients_to_table(self): # метод для загрузки клиентов в таблицу
        self.client_table.delete(*self.client_table.get_children()) # очищаем таблицу перед загрузкой новых данных
        for client in self.company.clients: # перебираем всех клиентов в компании
            self.client_table.insert("", "end", values=(client.name, client.cargo_weight, "Да" if client.is_vip else "Нет")) # добавляем клиента в таблицу
        self.client_table.bind("<Double-1>", self.edit_client) # двойной щелчок для редактирования клиента

    def add_client(self): # метод для добавления нового клиента
        self.client_window = tk.Toplevel(self.root)
        self.client_window.title("Добавить клиента")
        
        tk.Label(self.client_window, text="Имя клиента:").grid(row=0, column=0) # создаем метку для имени клиента
        self.client_name_entry = tk.Entry(self.client_window) # создаем поле ввода
        self.client_name_entry.grid(row=0, column=1)

        tk.Label(self.client_window, text="Вес груза:").grid(row=1, column=0)
        self.client_weight_entry = tk.Entry(self.client_window)
        self.client_weight_entry.grid(row=1, column=1)

        tk.Label(self.client_window, text="VIP статус:").grid(row=2, column=0)
        self.client_vip_var = tk.BooleanVar() # создаем переменную для хранения состояния VIP статуса
        self.client_vip_check = tk.Checkbutton(self.client_window, variable=self.client_vip_var) # создаем чекбокс для выбора VIP статуса
        self.client_vip_check.grid(row=2, column=1)

        tk.Button(self.client_window, text="Сохранить", command=self.save_client).grid(row=4, column=0, columnspan=1) # кнопка для сохранения нового клиента
        tk.Button(self.client_window, text="Отмена", command=self.client_window.destroy).grid(row=4, column=1, columnspan=2) # кнопка для закрытия окна без сохранения

    def save_client(self): # метод для сохранения данных нового клиента
        name = self.client_name_entry.get() # получаем данные клиента из поля ввода
        cargo_weight = self.client_weight_entry.get()
        vip_status = self.client_vip_var.get()

        if Validator.validate_client_data(name, cargo_weight, vip_status): # вызываем метод валидации
            cargo_weight = float(cargo_weight) # преобразуем вес в число после валидации
            client = Client(name, cargo_weight, vip_status) # создаем объект клиента с введенными данными
            self.company.add_client(client) # добавляем клиента в компанию
            self.load_clients_to_table() # обновляем таблицу клиентов
            self.save_data_to_json_clients(self.company.clients) # сохраняем обновленный список клиентов в JSON файл
            self.client_window.destroy() # закрываем окно добавления клиента
            self.status.config(text="Клиент добавлен") # обновляем статус с сообщением о добавлении клиента

    def edit_client(self, event): # метод для редактирования выбранного клиента
        selected_item = self.client_table.selection() # получаем выбранный элемент из таблицы клиентов
        if not selected_item: # если ничего не выбрано, выходим из метода
            return

        client_data = self.client_table.item(selected_item)['values'] # получаем данные выбранного клиента
        self.client_window = tk.Toplevel(self.root)
        self.client_window.title("Редактировать клиента")

        tk.Label(self.client_window, text="Имя клиента:").grid(row=0, column=0)
        self.client_name_entry = tk.Entry(self.client_window)
        self.client_name_entry.insert(0, client_data[0]) # заполняем поле ввода текущим именем клиента
        self.client_name_entry.grid(row=0, column=1)

        tk.Label(self.client_window, text="Вес груза:").grid(row=1, column=0)
        self.client_weight_entry = tk.Entry(self.client_window)
        self.client_weight_entry.insert(0, client_data[1]) # заполняем поле ввода текущим весом груза
        self.client_weight_entry.grid(row=1, column=1)

        tk.Label(self.client_window, text="VIP статус:").grid(row=2, column=0)
        self.client_vip_var = tk.BooleanVar(value=(client_data[2] == "Да")) 
        self.client_vip_check = tk.Checkbutton(self.client_window, variable=self.client_vip_var)
        self.client_vip_check.grid(row=2, column=1)

        tk.Button(self.client_window, text="Сохранить", command=lambda: self.save_edited_client(client_data[0])).grid(row=4, column=0, columnspan=1)
        tk.Button(self.client_window, text="Отмена", command=self.client_window.destroy).grid(row=4, column=1, columnspan=2)

    def delete_client(self): # метод для удаления выбранного клиента
        selected_item = self.client_table.selection() # получаем выбранный элемент из таблицы клиентов
        if not selected_item: # если ничего не выбрано, выводим предупреждение
            tk.messagebox.showwarning("Предупреждение", "Пожалуйста, выберите клиента для удаления.")
            return # выходим из метода

        client_name = self.client_table.item(selected_item)['values'][0] # получаем имя клиента для удаления
        self.company.clients = [client for client in self.company.clients if client.name != client_name] # удаляем клиента из списка
        self.load_clients_to_table()
        self.save_data_to_json_clients(self.company.clients)
        self.status.config(text="Клиент удален")

    def save_edited_client(self, old_name): # метод для сохранения изменений клиента
        name = self.client_name_entry.get()
        cargo_weight = self.client_weight_entry.get()
        vip_status = self.client_vip_var.get()

        if Validator.validate_client_data(name, cargo_weight, vip_status):
            cargo_weight = float(cargo_weight)
            for client in self.company.clients: # перебираем список клиентов компании для обновления данных
                if client.name == old_name: # если имя клиента совпадает с именем редактируемого клиента
                    client.name = name # обновляем имя клиента
                    client.cargo_weight = cargo_weight # обновляем вес груза клиента
                    client.is_vip = vip_status # обновляем статус VIP клиента
                    break

            self.load_clients_to_table()
            self.save_data_to_json_clients(self.company.clients)
            self.client_window.destroy()
            self.status.config(text="Данные клиента обновлены")

    def open_new_vehidesworkwindow(self): # метод для открытия окна работы с транспортными средствами
        self.root.withdraw()
        new_window = tk.Toplevel(self.root)
        new_window.title("Действия с транспортными средствами")
        new_window.geometry("820x595")
        new_window.resizable(width=False, height=False)
        new_window.configure(bg="white")

        self.frame = tk.Frame(new_window, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.transport_table = ttk.Treeview(self.frame, columns=("ID", "Тип", "Грузоподъемность"), show='headings')  # создаем таблицу для отображения транспортных средств с указанными столбиками
        self.transport_table.heading("ID", text="ID")
        self.transport_table.heading("Тип", text="Тип транспорта")
        self.transport_table.heading("Грузоподъемность", text="Грузоподъемность")
        self.transport_table.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        frame4 = tk.Frame(new_window, bg='gray15')
        frame4.place(relx=0.08, rely=0.029, relwidth=0.85, relheight=0.2)

        info_text4 = """
        Какую именно операцию Вы бы хотели 
        совершить?"""
        main_label = tk.Label(new_window, text=info_text4, font=("Arial", 16, 'bold'), fg="white", bg="gray15")
        main_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        btn_add_vehicle = tk.Button(new_window, text="Добавить транспорт", width=35, height=3, bg="black", fg="white", command=self.add_vehicle)
        btn_add_vehicle.place(x=150, y=180)

        btn_delete_vehicle = tk.Button(new_window, text="Удалить транспорт", width=35, height=3, bg="black", fg="white", command=self.delete_vehicle)
        btn_delete_vehicle.place(x=300, y=250)

        btn_return = tk.Button(new_window, text="Назад", width=35, height=3, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.place(x=450, y=180)

        self.load_transport_table() # загружаем данные о транспортных средствах в таблицу

    def load_transport_table(self): # метод для загрузки данных о транспортных средствах в таблицу
        self.transport_table.delete(*self.transport_table.get_children()) # очищаем таблицу перед загрузкой новых данных
        for vehicle in self.company.vehicles:
            if isinstance(vehicle, Truck):
                self.transport_table.insert("", "end", values=(len(self.transport_table.get_children()) + 1, "Грузовик", vehicle.capacity, vehicle.color))
            elif isinstance(vehicle, Train):
                self.transport_table.insert("", "end", values=(len(self.transport_table.get_children()) + 1, "Поезд", vehicle.capacity, vehicle.number_of_cars))
        self.transport_table.bind("<Double-1>", self.edit_vehicle) # двойной щелчок для редактирования транспортного средства

    def add_vehicle(self): # метод для добавления нового транспортного средства
        self.transport_window = tk.Toplevel(self.root)
        self.transport_window.title("Добавить транспорт")

        tk.Label(self.transport_window, text="Тип транспорта:").grid(row=0, column=0)
        self.transport_type = ttk.Combobox(self.transport_window, values=["Грузовик", "Поезд"]) # создаем выпадающий список для выбора типа транспорта
        self.transport_type.grid(row=0, column=1)
        self.transport_type.bind("<<ComboboxSelected>>", self.on_transport_type_selected) # привязываем обработчик выбора типа транспорта

        tk.Label(self.transport_window, text="Грузоподъемность:").grid(row=1, column=0)
        self.capacity = tk.Entry(self.transport_window)
        self.capacity.grid(row=1, column=1)

        self.color_label = tk.Label(self.transport_window, text="Цвет:")
        self.color_label.grid(row=2, column=0)
        self.color_entry = tk.Entry(self.transport_window)
        self.color_entry.grid(row=2, column=1)

        self.cars_label = tk.Label(self.transport_window, text="Количество вагонов:")
        self.cars_label.grid(row=3, column=0)
        self.cars_entry = tk.Entry(self.transport_window)
        self.cars_entry.grid(row=3, column=1)

        tk.Button(self.transport_window, text="Сохранить", command=self.save_transport).grid(row=4, column=0, columnspan=1)  
        tk.Button(self.transport_window, text="Отмена", command=self.transport_window.destroy).grid(row=4, column=1, columnspan=2)  

    def delete_vehicle(self): # метод для удаления транспортного средства
        selected_item = self.transport_table.selection() # получаем выбранный элемент из таблицы
        if not selected_item: # если ничего не выбрано, выводим предупреждение
            tk.messagebox.showwarning("Предупреждение", "Пожалуйста, выберите транспорт для удаления.")
            return

        vehicle_id = self.transport_table.item(selected_item)['values'][0] # получаем ID транспортного средства
        self.company.vehicles = [vehicle for vehicle in self.company.vehicles if vehicle.id != vehicle_id] # удаляем транспорт из списка, оставляя только те, у которых ID не совпадает с выбранным
        self.load_transport_table() # обновляем таблицу, чтобы отобразить изменения
        self.save_data_to_json_vehicles(self.company.vehicles) # сохраняем обновленный список транспортных средств в JSON файл
        self.status.config(text="Транспорт удален")

    def save_transport(self): # метод для сохранения нового транспортного средства
        vehicle_type = self.transport_type.get()
        capacity = self.capacity.get()
        color = self.color_entry.get()
        number_of_cars = self.cars_entry.get()

        if Validator.validate_vehicle_data(vehicle_type, capacity, color, number_of_cars):
            capacity = float(capacity) # преобразуем грузоподъемность в число
            if vehicle_type == "Грузовик":
                truck = Truck(capacity, color) # создаем экземпляр грузовика
                self.company.add_vehicle(truck) # добавляем грузовик в компанию
            elif vehicle_type == "Поезд":
                number_of_cars = int(number_of_cars) # преобразуем количество вагонов в целое число
                train = Train(capacity, number_of_cars) # создаем экземпляр поезда
                self.company.add_vehicle(train) # добавляем поезд в компанию

            self.load_transport_table() # обновляем таблицу транспортных средств
            self.save_data_to_json_vehicles(self.company.vehicles) # сохраняем данные о транспортных средствах в JSON файл
            self.transport_window.destroy() # закрываем окно добавления транспорта
            self.status.config(text="Транспорт добавлен")

    def edit_vehicle(self, event): # метод для редактирования выбранного транспортного средства
        selected_item = self.transport_table.selection() # получаем выбранный элемент из таблицы
        if not selected_item: # если ничего не выбрано, выходим из метода
            return

        vehicle_data = self.transport_table.item(selected_item)['values'] # получаем данные о выбранном транспортном средстве
        self.transport_window = tk.Toplevel(self.root)
        self.transport_window.title("Редактировать транспорт")

        tk.Label(self.transport_window, text="Тип транспорта:").grid(row=0, column=0)
        self.transport_type = ttk.Combobox(self.transport_window, values=["Грузовик", "Поезд"]) # создаем выпадающий список для выбора типа транспорта
        self.transport_type.set(vehicle_data[1]) # устанавливаем текущее значение
        self.transport_type.grid(row=0, column=1)
        self.transport_type.bind("<<ComboboxSelected>>", self.on_transport_type_selected) # привязываем обработчик выбора типа транспорта

        tk.Label(self.transport_window, text="Грузоподъемность:").grid(row=1, column=0)
        self.capacity = tk.Entry(self.transport_window)
        self.capacity.insert(0, vehicle_data[2]) # заполняем поле ввода текущей грузоподъемностью
        self.capacity.grid(row=1, column=1)

        self.color_label = tk.Label(self.transport_window, text="Цвет:")
        self.color_label.grid(row=2, column=0)
        self.color_entry = tk.Entry(self.transport_window)
        if len(vehicle_data) > 3: # если есть цвет (для грузовика)
            self.color_entry.insert(0, vehicle_data[3]) # заполняем поле ввода текущим цветом
        self.color_entry.grid(row=2, column=1)

        self.cars_label = tk.Label(self.transport_window, text="Количество вагонов:")
        self.cars_label.grid(row=3, column=0)
        self.cars_entry = tk.Entry(self.transport_window)
        if len(vehicle_data) > 4: # если есть количество вагонов (для поезда)
            self.cars_entry.insert(0, vehicle_data[4]) # заполняем поле ввода текущим количеством вагонов
        self.cars_entry.grid(row=3, column=1)

        self.on_transport_type_selected(None) # вызываем метод для удаления лишних полей в зависимости от типа транспорта

        tk.Button(self.transport_window, text="Сохранить", command=lambda: self.save_edited_vehicle(vehicle_data[0])).grid(row=4, column=0, columnspan=1)  
        tk.Button(self.transport_window, text="Отмена", command=self.transport_window.destroy).grid(row=4, column=1, columnspan=2)  

    def on_transport_type_selected(self, event): # метод для обработки выбора типа транспорта
        transport_type = self.transport_type.get() # получаем выбранный тип транспорта
        if transport_type == "Поезд": # если выбран поезд
            self.color_label.grid_remove() # скрываем метку и поле ввода для цвета
            self.color_entry.grid_remove() # скрываем поле ввода для цвета
            self.cars_label.grid() # показываем метку для количества вагонов
            self.cars_entry.grid() # показываем поле ввода для количества вагонов
        elif transport_type == "Грузовик": # если выбран грузовик
            self.cars_label.grid_remove() # скрываем метку и поле ввода для количества вагонов
            self.cars_entry.grid_remove() # скрываем поле ввода для количества вагонов
            self.color_label.grid() # показываем метку для цвета
            self.color_entry.grid() # показываем поле ввода для цвета

    def save_edited_vehicle(self, vehicle_id): # метод для сохранения изменений в редактируемом транспортном средстве
        transport_type = self.transport_type.get()
        capacity = self.capacity.get()
        color = self.color_entry.get()
        number_of_cars = self.cars_entry.get()

        if Validator.validate_vehicle_data(transport_type, capacity, color, number_of_cars): # вызываем метод валидации
            capacity = float(capacity)
            if transport_type == "Грузовик":
                for vehicle in self.company.vehicles:
                    if isinstance(vehicle, Truck) and vehicle.id == vehicle_id: # проверяем, совпадает ли ID
                        vehicle.capacity = capacity # обновляем грузоподъемность
                        vehicle.color = color # обновляем цвет
                        break
                        
            elif transport_type == "Поезд":
                number_of_cars = int(number_of_cars) # преобразуем количество вагонов в целое число
                for vehicle in self.company.vehicles:
                    if isinstance(vehicle, Train) and vehicle.id == vehicle_id: # проверяем, совпадает ли ID
                        vehicle.capacity = capacity # обновляем грузоподъемность
                        vehicle.number_of_cars = number_of_cars # обновляем количество вагонов
                        break

            self.load_transport_table() # обновляем таблицу, чтобы отобразить изменения
            self.save_data_to_json_vehicles(self.company.vehicles) 
            self.transport_window.destroy() # закрываем окно редактирования транспорта
            self.status.config(text="Данные транспорта обновлены")
            
    def open_new_cargo_distribution(self): # метод для открытия окна распределения груза
        self.root.withdraw() # скрываем главное окно
        new_window = tk.Toplevel(self.root)
        new_window.title("Распределение груза")
        new_window.geometry("820x595")

        btn_return = tk.Button(new_window, text="Назад", width=30, height=2, bg="black", fg="white", command=lambda: self.close_new_window(new_window))
        btn_return.pack(pady=20)

        self.result_text = tk.Text(new_window, height=20, width=80) 
        self.result_text.pack(pady=10)

        if not self.company.clients and not self.company.vehicles: # проверяем, есть ли клиенты и транспортные средства для распределения грузов
            self.result_text.insert(tk.END, "В данный момент нет клиентов и транспортных средств для распределения грузов.\n")
        elif not self.company.clients: # если список клиентов пуст
            self.result_text.insert(tk.END, "В данный момент нет клиентов для распределения грузов.\n")
        elif not self.company.vehicles: # если список транспортных средств пуст
            self.result_text.insert(tk.END, "В данный момент нет транспортных средств для распределения грузов.\n")
        else: # если есть и клиенты, и транспортные средства
            self.company.optimize_cargo_distribution() # распределяем груз между транспортными средствами
            self.result_text.insert(tk.END, "Распределение грузов выполнено:\n")
            for vehicle in self.company.vehicles: # проходим по всем транспортным средствам
                self.result_text.insert(tk.END, f"Транспортное средство: {vehicle}\n")
                if vehicle.clients_list: # если у транспортного средства есть загруженные клиенты
                    self.result_text.insert(tk.END, "Загруженные клиенты:\n")
                    for client in vehicle.clients_list: # проходим по списку загруженных клиентов
                        self.result_text.insert(tk.END, f" - Имя: {client.name}, Вес груза: {client.cargo_weight}, VIP-статус: {client.is_vip}\n")
                else: # если у транспортного средства нет загруженных клиентов
                    self.result_text.insert(tk.END, " - Не загружено ни одного клиента. Не хватает грузоподъемности или все клиенты уже загружены в другие транспортные средства :( \n")

    def close_new_window(self, window): # метод для закрытия указанного окна
        window.destroy() # закрываем указанное окно
        self.root.deiconify() # возвращаем главное окно на передний план (отображаем его)

if __name__ == "__main__": # проверяем, является ли данный файл основным модулем, который запускается
    root = tk.Tk() # создаем главное окно приложения
    app = TransportCompanyApp(root) # создаем экземпляр класса TransportCompanyApp, передавая главное окно в качестве аргумента
    root.mainloop() # запускаем главный цикл приложения
