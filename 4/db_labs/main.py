import tkinter as tk
from tkinter import ttk
import re
import psycopg2

WINDOW_DEFAULT_WIDTH = 1420
WINDOW_DEFAULT_HEIGHT = 780

class DbConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                dbname='postgres', 
                user='postgres', 
                host='localhost', 
                password='postgres',
                port='5432',
                client_encoding='win1251'
            )

            self.cursor = self.connection.cursor()

        except Exception as error:
            print("Error while connecting to PostgreSQL", error)

    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()

class WindowDefaultSize:
    def __init__(self, root):
        self.root = root
        self.root.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}+0+0")

class BackBtn:
    def __init__(self, root, back_command):
        self.root = root
        self.create_back_btn(self.root, back_command)

    def create_back_btn(self, root, back_command): 
        self.back_btn = tk.Button(root, text="Назад", width=6, height=1, font=("Arial", 12), command=back_command)
        self.back_btn.grid(row=0, column=0, sticky="nw")

class StartWindow(WindowDefaultSize):
    def __init__(self, root):
        super().__init__(root)
        self.root.title("Ремонт помещений")

        self.sign_up_btn = tk.Button(text="Регистрация", width=10, height=2, command=self.sign_up)
        self.sign_up_btn.place(x=200, y=220)
        self.sign_in_btn = tk.Button(text="Вход", width=10, height=2, command=self.sign_in)
        self.sign_in_btn.place(x=200, y=270)

        self.registration_canvas = tk.Canvas(bg="white", width=400, height=300)
        self.registration_canvas.place(x=320, y=110)
        self.registration_win_img = tk.PhotoImage(file="images/registration_win_img.png")

        self.registration_canvas.create_image(201, 151, image=self.registration_win_img)

    def sign_up(self):
        SignUpWindow(self.root)
        self.root.withdraw()

    def sign_in(self):
        SignInWindow(self.root)
        self.root.withdraw()

class SignUpWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
    
        super().__init__(self.root)

        self.root.title("Регистрация")
        BackBtn(self.root, self.back)

        self.error_label = None
        self.success_label = None
        self.parent = parent

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # surname
        self.surname_label = tk.Label(self.root, text="Фамилия", width=20, font=("Arial", 12))
        self.surname_label.place(x=228, y=120)
        self.surname = tk.Entry(self.root, width=20, font=("Arial", 12))
        self.surname.place(x=380, y=120)
        # name
        self.name_label = tk.Label(self.root, text="Имя", width=20, font=("Arial", 12))
        self.name_label.place(x=249, y=160)
        self.name = tk.Entry(self.root, width=20, font=("Arial", 12))
        self.name.place(x=380, y=160)
        # patronymic
        self.patronymic_label = tk.Label(self.root, text="Отчество", width=20, font=("Arial", 12))
        self.patronymic_label.place(x=227, y=200)
        self.patronymic = tk.Entry(self.root, width=20, font=("Arial", 12))
        self.patronymic.place(x=380, y=200)
        # phone
        self.phone_label = tk.Label(self.root, text="Телефон", width=20, font=("Arial", 12))
        self.phone_label.place(x=228, y=240)
        self.phone = tk.Entry(self.root, width=20, font=("Arial", 12))
        self.phone.insert(0, "+7")
        self.phone.place(x=380, y=240)
        self.phone.bind("<KeyRelease>", self.format_phone_number)
        # password
        self.password_label = tk.Label(self.root, text="Пароль", width=20, font=("Arial", 12))
        self.password_label.place(x=235, y=280)
        self.password = tk.Entry(self.root, width=20, font=("Arial", 12), show="*")
        self.password.place(x=380, y=280)
        self.show_password_btn = tk.Button(self.root, text="Показать пароль", font=("Arial", 12), width=14, height=1, command=self.show_password)
        self.show_password_btn.place(x=595, y=278)
        # password_again
        self.password_again_label = tk.Label(self.root, text="Повторите пароль", width=20, font=("Arial", 12))
        self.password_again_label.place(x=190, y=320)
        self.password_again = tk.Entry(self.root, width=20, font=("Arial", 12), show="*")
        self.password_again.place(x=380, y=320)
        # next_btn
        self.next_btn = tk.Button(self.root, text="Далее", font=("Arial", 12), width=14, height=1, command=lambda: self.values_check(self.root))
        self.next_btn.place(x=400, y=360)

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

    def on_close(self):
        self.root.destroy()
        self.parent.destroy()

    def show_password(self):
        if self.password['show'] == '*' or self.password_again['show'] == '*':
            self.password['show'] = ''
            self.password_again['show'] = ''
        else:
            self.password['show'] = '*'
            self.password_again['show'] = '*'

    def format_phone_number(self, event):

        phone_number = self.phone.get()
    
        digits = ''.join(filter(str.isdigit, phone_number))
        
        formatted_number = ''
        if len(digits) > 0:
            formatted_number += '+' + digits[:1]
        if len(digits) > 1:
            formatted_number += '(' + digits[1:4]
        if len(digits) > 4:
            formatted_number += ') ' + digits[4:7]
        if len(digits) > 7:
            formatted_number += '-' + digits[7:11]

        self.phone.delete(0, tk.END)
        self.phone.insert(0, formatted_number)

    def values_check(self, root):
        error_arr = []

        surname = self.surname.get()
        name = self.name.get()
        patronymic = self.patronymic.get()
        phone = self.phone.get()
        password = self.password.get()
        password_again = self.password_again.get()

        if (surname == "" or 
            name == "" or 
            patronymic == "" or 
            phone == "" or 
            password == "" or 
            password_again == ""):

            error_arr.append("Ошибка: Заполните все поля!")

        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', surname):
            error_arr.append("Ошибка: Неверный формат фамилии!")

        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', name):
            error_arr.append("Ошибка: Неверный формат имени!")

        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', patronymic):
            error_arr.append("Ошибка: Неверный формат отчества!")

        if len(phone) != 16:
            error_arr.append("Ошибка: Неверный формат номера телефона!")

        if len(password) < 8 or len(password_again) < 8:
            error_arr.append("Ошибка: Длина пароля минимум 8 символов!")

        if password != password_again:
            error_arr.append("Ошибка: Пароли не совпадают!")

        if len(error_arr) > 0:
            if self.error_label is not None and self.error_label.winfo_ismapped():
                self.error_label.destroy()
                self.error_label = None 

            if self.success_label is not None and self.success_label.winfo_ismapped():
                self.success_label.destroy()
                self.success_label = None

            error_message = "\n".join(error_arr)
            self.error_label = tk.Label(root, 
                                        bg="red", 
                                        font=("Arial", 12), 
                                        text=error_message)
            self.error_label.place(x=380, y=400)

        else:
            if self.error_label is not None and self.error_label.winfo_ismapped():
                self.error_label.destroy()

            self.db = DbConnection()
            
            self.db.cursor.execute(
                f"INSERT INTO client (name_, surname, patronymic, phone, password_) VALUES ('{name}', '{surname}', '{patronymic}', '{phone}', '{password}');")
            
            self.db.connection.commit()
            
            self.success_window = tk.Toplevel(root)
            self.success_window.title("Успех")
            super().__init__(self.success_window)
            self.success_label = tk.Label(self.success_window, 
                                          bg="#79d9a7", 
                                          font=("Arial", 12), 
                                          text="Регистрация прошла успешно!")
            self.success_label.place(x=5, y=5)
            self.success_btn = tk.Button(self.success_window, 
                                         font=("Arial", 12), 
                                         text="На главный экран", 
                                         command=self.start_window)
            self.success_btn.place(x=5, y=40)
            root.withdraw()
    
    def start_window(self):
        self.success_window.destroy()
        self.parent.deiconify()

class SignInWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Вход")
        super().__init__(self.root)

        BackBtn(self.root, self.back)
        self.parent = parent

        self.client_id = 0

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        self.phone_label = tk.Label(self.root, 
                                    text="Телефон", 
                                    font=("Arial", 12))
        self.phone_label.place(x=293, y=240)
        self.phone = tk.Entry(self.root, 
                              width=20, 
                              font=("Arial", 12))
        self.phone.insert(0, "+7")
        self.phone.place(x=380, y=240)
        self.phone.bind("<KeyRelease>", self.format_phone_number)

        self.password_label = tk.Label(self.root, 
                                       text="Пароль", 
                                       font=("Arial", 12))
        self.password_label.place(x=305, y=280)
        self.password = tk.Entry(self.root, width=20, font=("Arial", 12), show="*")
        self.password.place(x=380, y=280)
        self.show_password_btn = tk.Button(self.root, 
                                           text="Показать пароль", 
                                           font=("Arial", 12), 
                                           width=14, 
                                           height=1, 
                                           bg="white",
                                           command=self.show_password)
        self.show_password_btn.place(x=595, y=278)

        self.sign_in_btn = tk.Button(self.root, 
                                     text="Войти", 
                                     width=14, 
                                     height=1, 
                                     font=("Arial", 12),
                                     bg="white",
                                     command=self.sign_in)
        self.sign_in_btn.place(x=400, y=320)

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

    def on_close(self):
        self.root.destroy()
        self.parent.destroy()

    def format_phone_number(self, event):

        phone_number = self.phone.get()
    
        digits = ''.join(filter(str.isdigit, phone_number))
        
        formatted_number = ''
        if len(digits) > 0:
            formatted_number += '+' + digits[:1]
        if len(digits) > 1:
            formatted_number += '(' + digits[1:4]
        if len(digits) > 4:
            formatted_number += ') ' + digits[4:7]
        if len(digits) > 7:
            formatted_number += '-' + digits[7:11]

        self.phone.delete(0, tk.END)
        self.phone.insert(0, formatted_number)
    
    def show_password(self):
        if self.password['show'] == '*':
            self.password['show'] = ''
        else:
            self.password['show'] = '*'

    def sign_in(self):
        phone = self.phone.get()
        password = self.password.get()

        self.db = DbConnection()
        
        try:
            self.db.cursor.execute(
                "SELECT client_id FROM client WHERE phone = %s AND password_ = %s", (phone, password))
            
            result = self.db.cursor.fetchone()
            
            if result:
                self.client_id = result[0]
                MainWindow(self.root, self.client_id)        
                self.root.withdraw()
            else:
                self.error_label = tk.Label(self.root, bg="red", font=("Arial", 12), text="Ошибка: Неверно введены данные!")
                self.error_label.place(x=380, y=360)
        
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)

class MainWindow(WindowDefaultSize):
    def __init__(self, parent, client_id):
        self.root = tk.Toplevel(parent)
        self.root.title("Ремонт помещений")
        super().__init__(self.root)

        BackBtn(self.root, self.back)
        self.parent = parent

        self.client_id = client_id
        self.coast_per_unit_id = None

        self.db = DbConnection()
        self.chosen_services = []

        try:
            self.db.cursor.execute(
                "SELECT surname, name_, patronymic FROM client WHERE client_id = %s", (client_id,))
            
            result = self.db.cursor.fetchone()
            if result:
                surname, name_, patronymic = result
                self.client_name_label = tk.Label(self.root, 
                                                  text=f"Клиент: {surname} {name_} {patronymic}", 
                                                  bg="#deab3f",
                                                  font=("Arial", 12),
                                                  anchor="w")
                self.client_name_label.place(x=90, y=10)
            else:
                print("Клиент не найден")
                
        except Exception as e:
            print("Ошибка при получении данных клиента:", e)

        self.add_order_btn = tk.Button(self.root, 
                                     font=("Arial", 14), 
                                     text="Создать заказ",
                                     bg="green",
                                     command=self.add_order_func)
        self.add_order_btn.place(x=220, y=50)

        self.select_all_contracts_btn = tk.Button(self.root,
                                        font=("Arial", 14),
                                        text="Все заказы",
                                        command=self.select_all_contracts_func)
        self.select_all_contracts_btn.place(x=720, y=50)

    def add_order_func(self):
        self.add_servise_btn = tk.Button(self.root,
                                     font=("Arial", 14),
                                     text="Добавить услугу",
                                     command=self.add_servise_func)
        self.add_servise_btn.place(x=220, y=100)

        self.add_new_servise_btn = tk.Button(self.root, 
                                    font=("Arial", 14), 
                                    text="Добавить новую услугу", 
                                    command=self.add_servise_func)

        if self.add_order_btn.winfo_exists():
            self.add_order_btn.destroy()

        
    def add_servise_func(self):

        self.surfaces_arr = []
        self.servises_arr = []
        self.surfaces_data = {}
        self.servises_data = {}

        try:
            self.db.cursor.execute("SELECT surface_id, surface_name FROM surface")
            for surface_id, surface_name in self.db.cursor.fetchall():
                self.surfaces_arr.append(surface_name)
                self.surfaces_data[surface_name] = surface_id

            self.db.cursor.execute("SELECT servise_id, servise_name FROM servise")
            for servise_id, servise_name in self.db.cursor.fetchall():
                self.servises_data[servise_name] = servise_id

            self.selected_surface = tk.StringVar(self.root)
            self.selected_surface.set(self.surfaces_arr[0])

            self.surface_label = tk.Label(self.root, 
                                          text="Выберите поверхность:", 
                                          bg="#56999c",
                                          font=("Arial", 12), 
                                          anchor="w")
            self.surface_label.place(x=220, y=150)

            self.surface_dropdown = tk.OptionMenu(self.root, self.selected_surface, *self.surfaces_arr)
            self.surface_dropdown.config(font=("Arial", 12))
            self.surface_dropdown.place(x=220, y=180)

            self.selected_surface_btn = tk.Button(self.root,
                                                font=("Arial", 14),
                                                text="Далее",
                                                command=self.selected_surface_func)
            self.selected_surface_btn.place(x=220, y=220)

        except Exception as e:
            print(f"Ошибка: {e}")
            tk.Label(self.root, 
                     text="Ошибка загрузки данных", 
                     fg="red",
                     anchor="w").place(x=220, y=180)

    def selected_surface_func(self):
        self.surface_selected = self.selected_surface.get()
        self.surface_id = self.surfaces_data[self.surface_selected]

        self.surface_selected_label = tk.Label(self.root, 
                                               text=f"Вы выбрали поверхность: {self.surface_selected}", 
                                               font=("Arial", 12),
                                               anchor="w")
        self.surface_selected_label.place(x=220, y=260)
        
        try:
            self.db.cursor.execute("SELECT servise_id FROM coast_per_unit WHERE surface_id = %s", (self.surface_id,))
            
            for (servise_id,) in self.db.cursor.fetchall():
                self.db.cursor.execute("SELECT servise_name FROM servise WHERE servise_id = %s", (servise_id,))
                (servise_name,) = self.db.cursor.fetchone()
                self.servises_arr.append(servise_name)
            
            if not self.servises_arr:
                raise ValueError("Нет доступных услуг для выбранной поверхности")
            
            self.servise_label = tk.Label(self.root,
                                          text="Выберите услугу:",
                                          bg="#56999c",
                                          font=("Arial", 12),
                                          anchor="w")
            self.servise_label.place(x=220, y=290)
            
            self.selected_servise = tk.StringVar(self.root)
            self.selected_servise.set(self.servises_arr[0])

            self.servises_dropdown = tk.OptionMenu(self.root, self.selected_servise, *self.servises_arr)
            self.servises_dropdown.config(font=("Arial", 12))
            self.servises_dropdown.place(x=220, y=320)

            self.selected_servise_btn = tk.Button(self.root,
                                                font=("Arial", 14),
                                                text="Далее",
                                                command=self.selected_service_func)
            self.selected_servise_btn.place(x=220, y=355)
        
        except Exception as e:
            print(f"Ошибка: {e}")
            tk.Label(self.root, 
                     text=f"Ошибка: {str(e)}", 
                     fg="red",
                     anchor="w").place(x=220, y=180)

    def selected_service_func(self):
        self.servise_selected = self.selected_servise.get()
        self.servise_id = self.servises_data[self.servise_selected]
        self.servise_selected_label = tk.Label(self.root, 
                                               text=f"Вы выбрали услугу: {self.servise_selected}", 
                                               font=("Arial", 12),
                                               anchor="w")
        self.servise_selected_label.place(x=220, y=395)

        self.db.cursor.execute("SELECT unit_id, unit_name FROM unit")
        for unit_id, unit_name in self.db.cursor.fetchall():
            self.surfaces_arr.append(unit_name)
            self.surfaces_data[unit_name] = unit_id

        self.db.cursor.execute("SELECT unit_id FROM coast_per_unit WHERE surface_id=%s AND servise_id=%s", (self.surface_id, self.servise_id))
        self.unit_id = self.db.cursor.fetchone()

        self.db.cursor.execute("SELECT unit_name FROM unit WHERE unit_id=%s", (self.unit_id))
        self.selected_unit_name = self.db.cursor.fetchone()
        self.selected_unit_name = ''.join(map(str, self.selected_unit_name))

        self.num_of_unit_label = tk.Label(self.root,
                                          text=f"Введите количество ({self.selected_unit_name}):",
                                          bg="#56999c",
                                          font=("Arial", 12),
                                          anchor="w")
        self.num_of_unit_label.place(x=220, y=425)

        self.num_of_unit_entry = tk.Entry(self.root,
                                          font=("Arial", 12),
                                          width=10)
        self.num_of_unit_entry.place(x=220, y=455)

        self.selected_num_of_unit_btn = tk.Button(self.root,
                                                font=("Arial", 14),
                                                text="Далее",
                                                command=self.selected_num_of_unit_func)
        self.selected_num_of_unit_btn.place(x=220, y=485)

    def selected_num_of_unit_func(self):
        self.num_of_unit = self.num_of_unit_entry.get()

        if hasattr(self, 'selected_num_of_unit_error_label') and self.selected_num_of_unit_error_label.winfo_exists():
            self.selected_num_of_unit_error_label.destroy()

        if not self.num_of_unit:
            self.selected_num_of_unit_error_label = tk.Label(self.root,
                        font=("Arial", 12),
                        text="Ошибка: Введите значение",
                        fg="red",
                        anchor="e")
            self.selected_num_of_unit_error_label.place(x=320, y=455)
        else:
            try:
                num = float(self.num_of_unit)
                if num <= 0:
                    raise ValueError("Число должно быть положительным")
                    
                self.selected_num_of_unit_label = tk.Label(self.root, 
                        text=f"Вы ввели количество: {self.num_of_unit}", 
                        font=("Arial", 12),
                        anchor="w")
                self.selected_num_of_unit_label.place(x=220, y=525)
                
            except ValueError as e:
                self.selected_num_of_unit_error_label = tk.Label(self.root,
                        font=("Arial", 12),
                        text=f"Ошибка: {str(e)}",
                        fg="red",
                        anchor="e")
                self.selected_num_of_unit_error_label.place(x=320, y=455)

            # стоимость за одну услугу

            self.db.cursor.execute("SELECT coast FROM coast_per_unit WHERE surface_id=%s AND servise_id=%s AND unit_id=%s", 
                                (self.surface_id, self.servise_id, self.unit_id))
            self.coast_for_work = self.db.cursor.fetchone()

            self.coast_for_work = ''.join(map(str, self.coast_for_work))
            self.coast_for_work = float(self.coast_for_work) * int(self.num_of_unit)


            self.coast_for_servise_label = tk.Label(self.root,
                                                text=f"Стоимость услуги: {self.coast_for_work} ₽",
                                                bg="#82d078",
                                                font=('Arial', 12),
                                                anchor="w")
            self.coast_for_servise_label.place(x=220, y=555)

            self.order_confirmation_btn = tk.Button(self.root,
                                                    font=("Arial", 14),
                                                    text="Подтвердить услугу",
                                                    command=self.order_confirmation_func)
            self.order_confirmation_btn.place(x=220, y=585)

    def order_confirmation_func(self):
        print(f"Вы выбрали: Поверхность={self.surface_selected}, Услуга={self.servise_selected}, Стоимость={self.coast_for_work}")

        # выбранные атрибуты будут добавляться в массив (или список). после уже полного создания заказа данные окажутся в БД
        # будут добавляться в works_under_contract. 
        # contract_id реализуется позже
        # coast_per_unit_id будет хранить id, выбираемый по surface_id(self.surface_id) и servise_id(servise_id)
        # num_of_unit будет хранить self.selected_num_of_unit
        # coast_for_work будет хранить self.coast_for_work

        self.db.cursor.execute("SELECT coast_per_unit_id FROM coast_per_unit WHERE surface_id=%s AND servise_id=%s", 
                               (self.surface_id, self.servise_id))
        self.coast_per_unit_id = self.db.cursor.fetchone()

        self.one_chosen_servise = {
            'coast_per_unit_id': self.coast_per_unit_id,
            'num_of_unit': self.num_of_unit,
            'coast_for_work': self.coast_for_work
        }

        self.chosen_services.append(self.one_chosen_servise)
        print(f" одна услуга: {self.one_chosen_servise}")
        print(f"все услуги: {self.chosen_services}")

        self.clear_order_widgets()

    def clear_order_widgets(self):
        widgets = [
            'add_servise_btn', 'surface_label', 'surface_dropdown', 
            'selected_surface_btn', 'surface_selected_label',
            'servise_label', 'servises_dropdown', 'selected_servise_btn',
            'servise_selected_label', 'num_of_unit_label', 'num_of_unit_entry',
            'selected_num_of_unit_btn', 'selected_num_of_unit_label',
            'coast_for_servise_label', 'order_confirmation_btn'
        ]
        
        for widget_name in widgets:
            if hasattr(self, widget_name):
                getattr(self, widget_name).destroy()

        if self.one_chosen_servise:
            self.set_order_btn = tk.Button(self.root,
                                        font=("Arial", 14),
                                        text="Оформить заказ",
                                        bg="green",
                                        command=self.set_order_func)
            self.set_order_btn.place(x=220, y=50)

        self.add_new_servise_btn.place(x=220, y=100)

    def set_order_func(self):

        self.street_label = tk.Label(self.root,
                                     font=("Arial", 12),
                                     text="Введите название улицы")
        self.street_label.place(x=220, y=150)
        self.street_entry = tk.Entry(self.root,
                                     font=("Arial", 12),
                                     width=10)
        self.street_entry.place(x=220, y=170)
        self.num_of_street_btn = tk.Button(self.root,
                                     font=("Arial", 14),
                                     text="Далее",
                                     command=self.num_of_street_func)
        self.num_of_street_btn.place(x=220, y=190)

    def num_of_street_func(self):
        self.num_of_street_label = tk.Label(self.root,
                                     font=("Arial", 12),
                                     text="Введите номер дома")
        self.num_of_street_label.place(x=220, y=230)
        self.num_of_street_entry = tk.Entry(self.root,
                                     font=("Arial", 12),
                                     width=10)
        self.num_of_street_entry.place(x=220, y=270)
        self.floor_btn = tk.Button(self.root,
                                     font=("Arial", 14),
                                     text="Далее",
                                     command=self.floor_func)
        self.floor_btn.place(x=220, y=300)

    def floor_func(self):
        self.floor_label = tk.Label(self.root,
                                     font=("Arial", 12),
                                     text="Введите этаж")
        self.floor_label.place(x=220, y=330)
        self.floor_entry = tk.Entry(self.root,
                                     font=("Arial", 12),
                                     width=10)
        self.floor_entry.place(x=220, y=360)
        self.apartment_btn = tk.Button(self.root,
                                     font=("Arial", 14),
                                     text="Далее",
                                     command=self.apartment_func)
        self.apartment_btn.place(x=220, y=400)

    def apartment_func(self):
        self.apartment_label = tk.Label(self.root,
                                     font=("Arial", 12),
                                     text="Введите номер квартиры")
        self.apartment_label.place(x=220, y=430)
        self.apartment_entry = tk.Entry(self.root,
                                     font=("Arial", 12),
                                     width=10)
        self.apartment_entry.place(x=220, y=460)
        self.rooms_num_btn = tk.Button(self.root,
                                     font=("Arial", 14),
                                     text="Далее",
                                     command=self.rooms_num_func)
        self.rooms_num_btn.place(x=220, y=500)

    def rooms_num_func(self):
        self.rooms_num_label = tk.Label(self.root,
                                     font=("Arial", 12),
                                     text="Введите количество комнат для ремонта")
        self.rooms_num_label.place(x=220, y=530)
        self.rooms_num_entry = tk.Entry(self.root,
                                     font=("Arial", 12),
                                     width=10)
        self.rooms_num_entry.place(x=220, y=560)
        self.confirm_order_btn = tk.Button(self.root,
                                     font=("Arial", 14),
                                     text="Далее",
                                     command=self.confirm_order_func)
        self.confirm_order_btn.place(x=220, y=600)

    def confirm_order_func(self):
        street = self.street_entry.get()
        street_num = self.num_of_street_entry.get()
        floor = self.floor_entry.get()
        apartment = self.apartment_entry.get()
        rooms_num = self.rooms_num_entry.get()

        self.db.cursor.execute("""INSERT INTO space (street, home, floor_, apartment, rooms_num) 
                               VALUES (%s, %s, %s, %s, %s)
                               RETURNING space_id""", 
                               (street, street_num, floor, apartment, rooms_num,))
        self.db.connection.commit()
        
        space_id = self.db.cursor.fetchone()[0]
        total_coast = sum(servise['coast_for_work'] for servise in self.chosen_services)

        self.db.cursor.execute("""INSERT INTO contract (client_id, space_id, total_coast)
                               VALUES (%s, %s, %s)
                               RETURNING contract_id""",
                               (self.client_id, space_id, total_coast,))
        self.db.connection.commit()
        contract_id = self.db.cursor.fetchone()[0]

        for servise in self.chosen_services:
            self.db.cursor.execute("""INSERT INTO works_under_contract (contract_id, coast_per_unit_id, num_of_unit, coast_for_work)
                                VALUES (%s, %s, %s, %s)""",
                                (
                                    contract_id,
                                    servise['coast_per_unit_id'],
                                    servise['num_of_unit'],
                                    servise['coast_for_work'] 
                                ))
        self.db.connection.commit()

        self.clear_set_order_widgets()

    def clear_set_order_widgets(self):
        widgets = [
            'street_label', 'street_entry', 'num_of_street_btn',
            'num_of_street_label', 'num_of_street_entry', 'floor_btn',
            'floor_label', 'floor_entry', 'apartment_btn',
            'apartment_label', 'apartment_entry', 'rooms_num_btn',
            'rooms_num_label', 'rooms_num_entry', 'confirm_order_btn',
            'set_order_btn', 'add_new_servise_btn', 'add_order_btn'
        ]
        
        for widget_name in widgets:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                if widget.winfo_exists():
                    widget.destroy()

        self.chosen_services = []

        self.add_order_btn = tk.Button(self.root, 
                                    font=("Arial", 14), 
                                    text="Создать заказ",
                                    bg="green",
                                    command=self.add_order_func)
        self.add_order_btn.place(x=220, y=50)

        self.root.update()
        self.root.update()
        
    def select_all_contracts_func(self):
        AllContractsWindow(self.root, self.client_id, self.coast_per_unit_id)

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

    def on_close(self): # не робит
        self.root.destroy()
        self.parent.destroy()

class DeleteServise(WindowDefaultSize):
    pass

class AllContractsWindow(WindowDefaultSize):
    def __init__(self, parent, client_id, coast_per_unit_id):

        self.root = tk.Toplevel(parent)
        self.root.title("Ремонт помещений. Договоры")
        super().__init__(self.root)

        BackBtn(self.root, self.back)
        self.parent = parent
        self.client_id = client_id
        self.coast_per_unit_id = coast_per_unit_id
        self.db = DbConnection()

        # self.db.cursor.execute("SELECT * FROM contract WHERE client_id=%s", (self.client_id,))
        # all_client_contracts = self.db.cursor.fetchall()

        # self.contract_table = ttk.Treeview(self.root,
        #                         columns=("Номер договора", "ID клиента", "ID помещения", "Дата заключения", "Итоговая стоимость"),
        #                         show="headings")
        # self.contract_table.heading("Номер договора", text="Номер договора")
        # self.contract_table.heading("ID клиента", text="ID клиента")
        # self.contract_table.heading("ID помещения", text="ID помещения")
        # self.contract_table.heading("Дата заключения", text="Дата заключения")
        # self.contract_table.heading("Итоговая стоимость", text="Итоговая стоимость")

        # space_id_arr = []

        # for contract in all_client_contracts:
        #     contract_id, client_id1, space_id, conclusion_date, coast = contract
        #     self.contract_table.insert("", "end", values=(contract_id, client_id1, space_id, conclusion_date.strftime("%d.%m.%Y"), f"{float(coast):.2f} ₽")) 
        #     space_id_arr.append(space_id)
        
        # self.contract_table.grid(row=1, column=0, sticky="nw")



        # self.spaces_table = ttk.Treeview(self.root,
        #                                     columns=("ID помещения", "Street", "Номер дома", "Этаж", "Номер квартиры", "Количество комнат для ремонта"),
        #                                     show="headings")
        # self.spaces_table.heading("ID помещения", text="ID помещения")
        # self.spaces_table.heading("Street", text="Улица")
        # self.spaces_table.heading("Номер дома", text="Номер дома")
        # self.spaces_table.heading("Этаж", text="Этаж")
        # self.spaces_table.heading("Номер квартиры", text="Номер квартиры")
        # self.spaces_table.heading("Количество комнат для ремонта", text="Количество комнат для ремонта")

        # for space_id in space_id_arr:
        #     self.db.cursor.execute("SELECT * FROM space WHERE space_id=%s", (space_id,))
        #     all_client_spaces = self.db.cursor.fetchall()

        #     for space in all_client_spaces:
        #         space_id, street, home, floor_, apartment, rooms_num = space
        #         self.spaces_table.insert("", "end", values=(space_id, street, home, floor_, apartment, rooms_num))

        # self.spaces_table.grid(row=2, column=0, sticky="nw")

        self.db.cursor.execute("""SELECT 
                                    contract.contract_id,
                                    CONCAT(space.street, ', д. ', space.home, ', кв. ', space.apartment, ', ', space.floor_, ' этаж, ', space.rooms_num, ' комн.') AS space_info,
                                    contract.conclusion_date,
                                    contract.total_coast,
                                    CONCAT(surface.surface_name, ' - ', servise.servise_name) AS work_description,
                                    works_under_contract.num_of_unit,
                                    works_under_contract.coast_for_work
                                FROM 
                                    contract
                                JOIN 
                                    space ON contract.space_id = space.space_id
                                JOIN 
                                    works_under_contract ON contract.contract_id = works_under_contract.contract_id
                                JOIN 
                                    coast_per_unit ON works_under_contract.coast_per_unit_id = coast_per_unit.coast_per_unit_id
                                JOIN 
                                    surface ON coast_per_unit.surface_id = surface.surface_id
                                JOIN 
                                    servise ON coast_per_unit.servise_id = servise.servise_id
                                JOIN
                                    client ON contract.client_id = client.client_id
                                WHERE 
                                    client.client_id = 1
                                ORDER BY 
                                    contract.contract_id, work_description;""")
        
        all_contracts = self.db.cursor.fetchall()

        self.client_contracts_table = ttk.Treeview(self.root, 
                                                   columns=("Номер договора", "Помещение", "Дата заключения", "Итоговая стоимость",  "Услуга", "Количество единиц", "Стоимость за услугу"),
                                                   show="headings")
        self.client_contracts_table.heading("Номер договора", text="Номер договора")
        self.client_contracts_table.heading("Помещение", text="Помещение")
        self.client_contracts_table.heading("Дата заключения", text="Дата заключения")
        self.client_contracts_table.heading("Итоговая стоимость", text="Итоговая стоимость")
        self.client_contracts_table.heading("Услуга", text="Услуга")
        self.client_contracts_table.heading("Количество единиц", text="Количество единиц")
        self.client_contracts_table.heading("Стоимость за услугу", text="Стоимость за услугу")


        for contract in all_contracts:
            contract_id, space_info, conclusion_date, total_coast, work_description, num_of_unit, coast_for_work = contract
            self.client_contracts_table.insert("", "end", values=(contract_id, space_info, conclusion_date, total_coast, work_description, num_of_unit, coast_for_work))
        self.client_contracts_table.grid(row=1, column=0, sticky="nw")
        
    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class AllServises(WindowDefaultSize):
    pass

if __name__ == "__main__":
    root = tk.Tk()
    StartWindow(root)
    root.mainloop()
