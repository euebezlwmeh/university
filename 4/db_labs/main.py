import tkinter as tk
from tkinter import ttk
import re
import psycopg2

# АДМИНИСТРАТОР
# +7(111) 111-1111
# admin_cool
# id 13

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
                if self.client_id == 13:
                    AdminWindow(self.root, self.client_id)
                else:
                    MainWindow(self.root, self.client_id)        
                self.root.withdraw()
            else:
                self.error_label = tk.Label(self.root, bg="red", font=("Arial", 12), text="Ошибка: Неверно введены данные!")
                self.error_label.place(x=380, y=360)
        
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)

class AdminWindow(WindowDefaultSize):
    def __init__(self, parent, client_id):
        self.root = tk.Toplevel(parent)
        self.root.title("Администратор")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)
        self.parent = parent
        self.client_id = client_id

        self.all_client_btn = tk.Button(self.root, 
                                        text="Все клиенты", 
                                        width=10, 
                                        height=1, 
                                        font=("Arial", 12), 
                                        command=self.all_client_func)
        self.all_client_btn.grid(row=1, column=0, sticky="nw")

        self.first_10_client_btn = tk.Button(self.root, 
                                             text="Первые 10 клиентов", 
                                             width=20, 
                                             height=1, 
                                             font=("Arial", 12), 
                                             command=self.first_10_client_func)
        self.first_10_client_btn.grid(row=2, column=0, sticky="nw")

        self.last_15_client_btn = tk.Button(self.root,
                                             text="Последние 15 клиентов",
                                             width=20, 
                                             height=1, 
                                             font=("Arial", 12), 
                                             command=self.last_15_client_func)
        self.last_15_client_btn.grid(row=3, column=0, sticky="nw")

        self.delete_coast_per_unit_btn = tk.Button(self.root,
                                                   text="Удалить услугу",
                                                   width=20, 
                                                   height=1, 
                                                   font=("Arial", 12), 
                                                   command=self.delete_coast_per_unit_func)
        self.delete_coast_per_unit_btn.grid(row=4, column=0, sticky="nw")

        self.unique_space_id_btn = tk.Button(self.root,
                                             text="Помещения одного клиента",
                                             width=25, 
                                             height=1, 
                                             font=("Arial", 12), 
                                             command=self.unique_space_id_func) 
        self.unique_space_id_btn.grid(row=5, column=0, sticky="nw")

        self.contract_coast_btn = tk.Button(self.root,
                                            text="Оценка стоимости договоров",
                                            width=25,
                                            height=1,
                                            font=("Arial", 12),
                                            command=self.contract_coast_func)
        self.contract_coast_btn.grid(row=6, column=0, sticky="nw")

        self.search_by_surname_btn = tk.Button(self.root,
                                                text="Поиск по фамилии",
                                                width=25,
                                                height=1,
                                                font=("Arial", 12),
                                                command=self.search_by_surname_func)      
        self.search_by_surname_btn.grid(row=7, column=0, sticky="nw")         

        self.by_client_coast_btn = tk.Button(self.root, 
                                            text="Сортировка по стоимости договора клиента",
                                            width=40,
                                            height=1,
                                            font=("Arial", 12),
                                            command=self.by_client_coast_func)
        self.by_client_coast_btn.grid(row=8, column=0, sticky="nw")

        self.contract_by_conclusion_date_btn = tk.Button(self.root,
                                                         text="Договор по дате и стоимости",
                                                         width=25,
                                                         height=1,
                                                         font=("Arial", 12),
                                                         command=self.contract_by_conclusion_date_func)
        self.contract_by_conclusion_date_btn.grid(row=9, column=0, sticky="nw")

        self.contracts_with_more_one_work_btn = tk.Button(self.root, 
                                                          text="Договоры, в которых более одной работы",
                                                          width=40,
                                                          height=1,
                                                          font=("Arial", 12),
                                                          command=self.contracts_with_more_one_work_func)
        self.contracts_with_more_one_work_btn.grid(row=10, column=0, sticky="nw")

        self.count_contracts_for_every_client_btn = tk.Button(self.root,
                                                          text="Количество договоров для каждого пользователя",
                                                          width=50,
                                                          height=1,
                                                          font=("Arial", 12),
                                                          command=self.count_contracts_for_every_client_func)
        self.count_contracts_for_every_client_btn.grid(row=11, column=0, sticky="nw")

        self.anniversary_btn = tk.Button(self.root,
                                            text="Юбилеи клиентов",
                                            width=20,
                                            height=1,
                                            font=("Arial", 12),
                                            command=self.anniversary_func)
        self.anniversary_btn.grid(row=12, column=0, sticky="nw")

        self.incorrect_phone_btn = tk.Button(self.root,
                                           text="Некорректные номера телефона",
                                            width=30,
                                            height=1,
                                            font=("Arial", 12),
                                            command=self.incorrect_phone_func)
        self.incorrect_phone_btn.grid(row=13, column=0, sticky="nw")

        self.search_client_by_pk_btn = tk.Button(self.root,
                                           text="Поиск клиента по ID",
                                            width=20,
                                            height=1,
                                            font=("Arial", 12),
                                            command=self.search_client_by_pk_func)
        self.search_client_by_pk_btn.grid(row=14, column=0, sticky="nw")

    def all_client_func(self):
        AllClientWindow(self.root)

    def first_10_client_func(self):
        First10ClientWindow(self.root)

    def last_15_client_func(self):
        Last15ClientWindow(self.root)

    def delete_coast_per_unit_func(self):
        DeleteCoastPerUnitWindow(self.root)

    def unique_space_id_func(self):
        UniqueSpaceIdWindow(self.root)

    def contract_coast_func(self):
        ContractCoastWindow(self.root)

    def search_by_surname_func(self):
        SearchBySurnameWindow(self.root)

    def by_client_coast_func(self):
        ByClientCoastWindow(self.root)

    def contract_by_conclusion_date_func(self):
        ContractByConclusionDateWindow(self.root)

    def contracts_with_more_one_work_func(self):
        ContractsWithMoreOneWorkWindow(self.root)

    def count_contracts_for_every_client_func(self):
        CountContractForEveryClientWindow(self.root)

    def anniversary_func(self):
        AnniversaryWindow(self.root)

    def incorrect_phone_func(self):
        IncorrectPhoneWindow(self.root)

    def search_client_by_pk_func(self):
        SearchClientByPK(self.root)

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class AllClientWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Список клиентов")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.db.cursor.execute("SELECT * FROM client")
        all_clients = self.db.cursor.fetchall()

        all_clients_table = ttk.Treeview(self.root, 
                                              columns=("client_id", "Фамилия", "Имя", "Отчество", "Телефон", "Пароль"),
                                              show="headings")
        all_clients_table.heading("client_id", text="client_id")
        all_clients_table.heading("Фамилия", text="Фамилия")
        all_clients_table.heading("Имя", text="Имя")
        all_clients_table.heading("Отчество", text="Отчество")
        all_clients_table.heading("Телефон", text="Телефон")
        all_clients_table.heading("Пароль", text="Пароль")

        for client in all_clients:
            all_clients_table.insert("", "end", values=client)

        all_clients_table.grid(row=1, column=0, sticky="nw")

        self.db.connection.commit()

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class First10ClientWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Первые 10 клиентов")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.db.cursor.execute("SELECT * FROM client ORDER BY client_id ASC LIMIT 10")
        all_clients = self.db.cursor.fetchall()

        all_clients_table = ttk.Treeview(self.root, 
                                              columns=("client_id", "Фамилия", "Имя", "Отчество", "Телефон", "Пароль"),
                                              show="headings")
        all_clients_table.heading("client_id", text="client_id")
        all_clients_table.heading("Фамилия", text="Фамилия")
        all_clients_table.heading("Имя", text="Имя")
        all_clients_table.heading("Отчество", text="Отчество")
        all_clients_table.heading("Телефон", text="Телефон")
        all_clients_table.heading("Пароль", text="Пароль")

        for client in all_clients:
            all_clients_table.insert("", "end", values=client)

        all_clients_table.grid(row=1, column=0, sticky="nw")

        self.db.connection.commit()
    
    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class Last15ClientWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Последние 15 клиентов")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.db.cursor.execute("SELECT * FROM client ORDER BY client_id DESC LIMIT 15")
        all_clients = self.db.cursor.fetchall()

        all_clients_table = ttk.Treeview(self.root, 
                                              columns=("client_id", "Фамилия", "Имя", "Отчество", "Телефон", "Пароль"),
                                              show="headings")
        all_clients_table.heading("client_id", text="client_id")
        all_clients_table.heading("Фамилия", text="Фамилия")
        all_clients_table.heading("Имя", text="Имя")
        all_clients_table.heading("Отчество", text="Отчество")
        all_clients_table.heading("Телефон", text="Телефон")
        all_clients_table.heading("Пароль", text="Пароль")

        for client in all_clients:
            all_clients_table.insert("", "end", values=client)

        all_clients_table.grid(row=1, column=0, sticky="nw")

        self.db.connection.commit()

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class DeleteCoastPerUnitWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Удалить услугу")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.enter_coast_per_unit_label = tk.Label(self.root, text="Введите id услуги")
        self.enter_coast_per_unit_label.grid(row=1, column=0, sticky="nw")
        self.enter_coast_per_unit_entry = tk.Entry(self.root)
        self.enter_coast_per_unit_entry.grid(row=1, column=1, sticky="nw")
        self.confirm_deleting_btn = tk.Button(self.root,
                                          text="Удалить услугу",
                                          font=("Arial", 12), 
                                          command=self.confirm_deleting_func)
        self.confirm_deleting_btn.grid(row=2, column=0, sticky="nw")

    def confirm_deleting_func(self):
        self.db.cursor.execute("DELETE FROM coast_per_unit WHERE coast_per_unit_id=%s", (self.enter_coast_per_unit_entry.get(),))
        self.db.connection.commit()

        self.success_label = tk.Label(self.root, text="Успешно", bg="green")
        self.success_label.grid(row=3, column=1, sticky="nw")

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class UniqueSpaceIdWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Помещения клиента")
        super().__init__(self.root)
        self.db = DbConnection()
        BackBtn(self.root, self.back)

        self.enter_client_label = tk.Label(self.root, text="Введите id клиента")
        self.enter_client_label.grid(row=1, column=0, sticky="nw")
        self.enter_client_entry = tk.Entry(self.root)
        self.enter_client_entry.grid(row=2, column=0, sticky="nw")
        self.confirm_btn = tk.Button(self.root,
                                    text="Показать помещения",
                                    font=("Arial", 12), 
                                    command=self.client_servise)
        self.confirm_btn.grid(row=3, column=0, sticky="nw")

    def client_servise(self):
        self.db.cursor.execute("""SELECT s.space_id, s.street, s.home, s.floor_, s.apartment, s.rooms_num
                                    FROM contract c
                                    JOIN space s ON c.space_id = s.space_id
                                    WHERE c.client_id = %s""", (self.enter_client_entry.get(),))
        all_client_spaces = self.db.cursor.fetchall()

        all_client_space_table = ttk.Treeview(self.root, 
                                        columns=("space_id", "street", "home", "floor_", "apartment", "rooms_num"),
                                        show="headings")
        all_client_space_table.heading("space_id", text="space_id")
        all_client_space_table.heading("street", text="Улица")
        all_client_space_table.heading("home", text="Дом")
        all_client_space_table.heading("floor_", text="Этаж")
        all_client_space_table.heading("apartment", text="Квартира")
        all_client_space_table.heading("rooms_num", text="Количество комнат")

        for space in all_client_spaces:
            all_client_space_table.insert("", "end", values=space)

        all_client_space_table.grid(row=4, column=0, sticky="nw")

        self.db.connection.commit()

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class ContractCoastWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Оценка стоимости договоров")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.db.cursor.execute("SELECT MAX(total_coast), MIN(total_coast), AVG(total_coast) FROM contract")
        coasts = self.db.cursor.fetchall()

        coasts_table = ttk.Treeview(self.root, 
                                    columns=("MAX", "MIN", "AVG"), 
                                    show="headings")
        
        coasts_table.heading("MAX", text="Максимальное значение")
        coasts_table.heading("MIN", text="Минимальное значение")
        coasts_table.heading("AVG", text="Среднее значение")

        for coast in coasts:
            coasts_table.insert("", "end", values=coast)

        coasts_table.grid(row=1, column=0, sticky="nw")

        self.db.connection.commit()

        self.more_coast_btn = tk.Button(self.root, text="Стоимость договора больше:", command=self.more_coast_func)
        self.more_coast_btn.grid(row=2, column=0, sticky="nw")
        self.more_coast_entry = tk.Entry(self.root)
        self.more_coast_entry.grid(row=3, column=0, sticky="nw")
        self.less_coast_btn = tk.Button(self.root, text="Стоимость договора меньше:", command=self.less_coast_func)
        self.less_coast_btn.grid(row=4, column=0, sticky="nw")
        self.less_coast_entry = tk.Entry(self.root)
        self.less_coast_entry.grid(row=5, column=0, sticky="nw")
        self.between_coast_btn = tk.Button(self.root, text="Стоимость договора между:", command=self.between_coast_func)
        self.between_coast_btn.grid(row=6, column=0, sticky="nw")
        self.between_min_coast_entry = tk.Entry(self.root)
        self.between_min_coast_entry.grid(row=7, column=0, sticky="nw")
        self.and_label = tk.Label(self.root, text="И")
        self.and_label.grid(row=8, column=0, sticky="nw")
        self.between_max_coast_entry = tk.Entry(self.root)
        self.between_max_coast_entry.grid(row=9, column=0, sticky="nw")

    def more_coast_func(self):
        self.db.cursor.execute("SELECT * FROM contract WHERE total_coast > %s", (self.more_coast_entry.get(),))
        all_contract = self.db.cursor.fetchall()

        all_contract_table = ttk.Treeview(self.root, 
                                        columns=("contract_id", "client_id", "space_id", "conclusion_date", "total_coast", "completion_date", "contract_status_id"),
                                        show="headings")
        all_contract_table.heading("contract_id", text="contract_id")
        all_contract_table.heading("client_id", text="client_id")
        all_contract_table.heading("space_id", text="space_id")
        all_contract_table.heading("conclusion_date", text="Дата заключения")
        all_contract_table.heading("total_coast", text="Стоимость")
        all_contract_table.heading("completion_date", text="Дата завершения")
        all_contract_table.heading("contract_status_id", text="id договора")

        for contract in all_contract:
            all_contract_table.insert("", "end", values=contract)

        all_contract_table.grid(row=1, column=0, sticky="nw")

        self.db.connection.commit()

    def less_coast_func(self):
        self.db.cursor.execute("SELECT * FROM contract WHERE total_coast < %s", (self.less_coast_entry.get(),))
        all_contract = self.db.cursor.fetchall()

        all_contract_table = ttk.Treeview(self.root, 
                                        columns=("contract_id", "client_id", "space_id", "conclusion_date", "total_coast", "completion_date", "contract_status_id"),
                                        show="headings")
        all_contract_table.heading("contract_id", text="contract_id")
        all_contract_table.heading("client_id", text="client_id")
        all_contract_table.heading("space_id", text="space_id")
        all_contract_table.heading("conclusion_date", text="Дата заключения")
        all_contract_table.heading("total_coast", text="Стоимость")
        all_contract_table.heading("completion_date", text="Дата завершения")
        all_contract_table.heading("contract_status_id", text="id договора")

        for contract in all_contract:
            all_contract_table.insert("", "end", values=contract)

        all_contract_table.grid(row=1, column=0, sticky="nw")

        self.db.connection.commit()

    def between_coast_func(self):
        self.db.cursor.execute("SELECT * FROM contract WHERE total_coast BETWEEN %s AND %s", (self.between_min_coast_entry.get(), self.between_max_coast_entry.get()))
        all_contract = self.db.cursor.fetchall()

        all_contract_table = ttk.Treeview(self.root, 
                                        columns=("contract_id", "client_id", "space_id", "conclusion_date", "total_coast", "completion_date", "contract_status_id"),
                                        show="headings")
        all_contract_table.heading("contract_id", text="contract_id")
        all_contract_table.heading("client_id", text="client_id")
        all_contract_table.heading("space_id", text="space_id")
        all_contract_table.heading("conclusion_date", text="Дата заключения")
        all_contract_table.heading("total_coast", text="Стоимость")
        all_contract_table.heading("completion_date", text="Дата завершения")
        all_contract_table.heading("contract_status_id", text="id договора")

        for contract in all_contract:
            all_contract_table.insert("", "end", values=contract)

        all_contract_table.grid(row=1, column=0, sticky="nw")

        self.db.connection.commit()

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class SearchBySurnameWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Поиск по фамилии")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=1, column=0, sticky="nw")
        self.search_btn = tk.Button(self.root, text="Поиск", command=self.search_func)
        self.search_btn.grid(row=2, column=0, sticky="nw")

        
    def search_func(self):
        self.db.cursor.execute(f"SELECT * FROM client WHERE surname LIKE '{self.search_entry.get()}%';")
        all_clients = self.db.cursor.fetchall()

        all_clients_table = ttk.Treeview(self.root, 
                                        columns=("client_id", "Фамилия", "Имя", "Отчество", "Телефон", "Пароль"),
                                        show="headings")
        all_clients_table.heading("client_id", text="client_id")
        all_clients_table.heading("Фамилия", text="Фамилия")
        all_clients_table.heading("Имя", text="Имя")
        all_clients_table.heading("Отчество", text="Отчество")
        all_clients_table.heading("Телефон", text="Телефон")
        all_clients_table.heading("Пароль", text="Пароль")

        for client in all_clients:
            all_clients_table.insert("", "end", values=client)

        all_clients_table.grid(row=3, column=0, sticky="nw")

        self.db.connection.commit()

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class ByClientCoastWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Сортировка по стоимости договора у клиента")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.client_id_label = tk.Label(self.root, text="Введите id клиента")
        self.client_id_label.grid(row=1, column=0)
        self.client_id_entry = tk.Entry(self.root)
        self.client_id_entry.grid(row=2, column=0)
        self.coast_min_label = tk.Label(self.root, text="Введите нижнюю границу")
        self.coast_min_label.grid(row=3, column=0)
        self.coast_min_label_entry = tk.Entry(self.root)
        self.coast_min_label_entry.grid(row=4, column=0)
        self.coast_max_label = tk.Label(self.root, text="Введите верхнюю границу")
        self.coast_max_label.grid(row=5, column=0)
        self.coast_max_label_entry = tk.Entry(self.root)
        self.coast_max_label_entry.grid(row=6, column=0)
        self.by_client_btn = tk.Button(self.root, text="До и после диапазона", command=self.and_func)
        self.by_client_btn.grid(row=7, column=0)
        self.by_client_btn = tk.Button(self.root, text="В диапазоне", command=self.between_func)
        self.by_client_btn.grid(row=8, column=0)

    def and_func(self):
        self.db.cursor.execute("""SELECT * FROM contract WHERE client_id=%s AND (total_coast < %s OR total_coast > %s) 
                               AND total_coast IS NOT NULL""", 
                               (self.client_id_entry.get(), 
                                self.coast_min_label_entry.get(), 
                                self.coast_max_label_entry.get(),))
        contracts = self.db.cursor.fetchall()
        self.table_func(contracts)
        self.db.connection.commit()

    def between_func(self):
        self.db.cursor.execute("SELECT * FROM contract WHERE client_id=%s AND total_coast BETWEEN %s AND %s", 
                               (self.client_id_entry.get(), self.coast_min_label_entry.get(), self.coast_max_label_entry.get(),))
        contracts = self.db.cursor.fetchall()
        self.table_func(contracts)
        self.db.connection.commit()

    def table_func(self, contracts):
        all_contracts_table = ttk.Treeview(self.root, 
                                columns=("contract_id", "space_id", "conclusion_date", "total_coast", "completion_date"),
                                show="headings")
        all_contracts_table.heading("contract_id", text="contract_id")
        all_contracts_table.heading("space_id", text="space_id")
        all_contracts_table.heading("conclusion_date", text="Дата заключения")
        all_contracts_table.heading("total_coast", text="Итоговая стоимость")
        all_contracts_table.heading("completion_date", text="Дата завершения")

        for contract in contracts:
            all_contracts_table.insert("", "end", values=contract)

        all_contracts_table.grid(row=9, column=0, sticky="nw")

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class ContractByConclusionDateWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Договоры по дате заключения и стоимости")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.db.cursor.execute("SELECT * FROM contract ORDER BY conclusion_date DESC, total_coast ASC")
        contracts = self.db.cursor.fetchall()

        self.table_func(contracts)
        self.db.connection.commit()

    def table_func(self, contracts):
        frame = ttk.Frame(self.root)
        frame.grid(row=1, column=0, sticky="nsew")

        all_contracts_table = ttk.Treeview(frame, 
                                columns=("contract_id", "client_id", "space_id", "conclusion_date", "total_coast", "completion_date"),
                                show="headings")

        all_contracts_table.heading("contract_id", text="ID договора")
        all_contracts_table.heading("client_id", text="ID клиента")
        all_contracts_table.heading("space_id", text="ID помещения")
        all_contracts_table.heading("conclusion_date", text="Дата заключения")
        all_contracts_table.heading("total_coast", text="Итоговая стоимость")
        all_contracts_table.heading("completion_date", text="Дата завершения")

        for col in all_contracts_table["columns"]:
            all_contracts_table.column(col, width=100, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=all_contracts_table.yview)
        all_contracts_table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        all_contracts_table.pack(side="left", fill="both", expand=True)

        for contract in contracts:
            all_contracts_table.insert("", "end", values=contract)

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class ContractsWithMoreOneWorkWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Договоры, в которых более одной работы")
        super().__init__(self.root)

        BackBtn(self.root, self.back)

        self.db = DbConnection()

        self.db.cursor.execute("SELECT contract_id, total_coast FROM contract EXCEPT SELECT contract_id, coast_for_work " \
                                "FROM works_under_contract ORDER BY contract_id ASC")
        contracts = self.db.cursor.fetchall()

        all_contracts_table = ttk.Treeview(self.root, 
                        columns=("contract_id", "total_coast"),
                        show="headings")
        all_contracts_table.heading("contract_id", text="contract_id")
        all_contracts_table.heading("total_coast", text="Итоговая стоимость")

        for contract in contracts:
            all_contracts_table.insert("", "end", values=contract)

        all_contracts_table.grid(row=1, column=0, sticky="nw")
 
    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class CountContractForEveryClientWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Количество договоров для каждого пользователя")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.db.cursor.execute("SELECT client_id, COUNT(*) FROM contract GROUP BY client_id ORDER BY client_id")
        contracts = self.db.cursor.fetchall()

        all_contracts_table = ttk.Treeview(self.root, 
                        columns=("client_id", "count"),
                        show="headings")
        all_contracts_table.heading("client_id", text="client_id")
        all_contracts_table.heading("count", text="Количество договоров")

        for contract in contracts:
            all_contracts_table.insert("", "end", values=contract)

        all_contracts_table.grid(row=1, column=0, sticky="nw")

        self.label = tk.Label(self.root, text="Клиенты с более чем одним договором").grid(row=2, column=0, sticky="nw")

        self.db.cursor.execute("""SELECT DISTINCT c.client_id,
                                cl.surname || ' ' || cl.name_ || ' ' || COALESCE(cl.patronymic, '') AS full_name
                                FROM contract c
                                JOIN contract c2 ON c.client_id = c2.client_id AND c.space_id != c2.space_id
                                JOIN client cl ON c.client_id = cl.client_id
                                ORDER BY c.client_id ASC""")
        clients = self.db.cursor.fetchall()

        clients_table = ttk.Treeview(self.root, 
                columns=("client_id", "name"),
                show="headings")
        clients_table.heading("client_id", text="client_id")
        clients_table.heading("name", text="ФИО")

        for client in clients:
            clients_table.insert("", "end", values=client)

        clients_table.grid(row=3, column=0, sticky="nw")

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class AnniversaryWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Юбилеи в следующем месяце")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.db.cursor.execute("""SELECT CONCAT(surname, ' ', LEFT(name_, 1), '.'),
                               EXTRACT(YEAR FROM AGE(birthdate)) + 1,
                               TO_CHAR(birthdate, 'DD.MM.YYYY'),
                               TO_CHAR(
                                    birthdate + (EXTRACT(YEAR FROM AGE(birthdate))) * INTERVAL '1 year' + INTERVAL '1 year',
                                    'DD.MM.YYYY'
                               )
                               FROM client
                               WHERE 
                                    EXTRACT(MONTH FROM birthdate) = EXTRACT(MONTH FROM CURRENT_DATE + INTERVAL '1 month')
                                    AND EXTRACT(YEAR FROM AGE(birthdate))::integer % 5 = 4
                                    AND birthdate IS NOT NULL
                                ORDER BY 
                                    surname, name_""")
        anniversary_clients = self.db.cursor.fetchall()

        all_clients_table = ttk.Treeview(self.root, 
                        columns=("name", "age", "birthdate", "anniversary_date"),
                        show="headings")
        all_clients_table.heading("name", text="Имя")
        all_clients_table.heading("age", text="Возраст")
        all_clients_table.heading("birthdate", text="Дата рождения")
        all_clients_table.heading("anniversary_date", text="Дата юбилея")

        for clients in anniversary_clients:
            all_clients_table.insert("", "end", values=clients)

        all_clients_table.grid(row=1, column=0, sticky="nw")  
        

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

class IncorrectPhoneWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Некорректные номера телефона")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)

        self.db.cursor.execute("SELECT * FROM client WHERE phone NOT LIKE '%\\(%' ESCAPE '\\' ORDER BY client_id ASC")

        data = self.db.cursor.fetchall()

        all_clients_table = ttk.Treeview(self.root, 
                columns=("client_id", "name_", "surname",  "patronymic", "phone", "password_", "birthdate"),
                show="headings")
        all_clients_table.heading("client_id", text="ID")
        all_clients_table.heading("surname", text="Фамилия")
        all_clients_table.heading("name_", text="Имя")
        all_clients_table.heading("patronymic", text="Отчество")
        all_clients_table.heading("phone", text="Телефон")
        all_clients_table.heading("password_", text="Пароль")
        all_clients_table.heading("birthdate", text="Дата рождения")

        for clients in data:
            all_clients_table.insert("", "end", values=clients)

        all_clients_table.grid(row=1, column=0, sticky="nw") 

    def back(self):
        self.root.destroy()
        self.root.master.deiconify() 

class SearchClientByPK(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Поиск клиента по ID")
        super().__init__(self.root)
        self.db = DbConnection()

        BackBtn(self.root, self.back)
        
        self.search_client_by_id_label = tk.Label(self.root, text="Введите ID:").grid(row=1, column=0, sticky="nw")
        self.search_client_by_id_entry = tk.Entry(self.root)
        self.search_client_by_id_entry.grid(row=2, column=0, sticky="nw")
        self.search_client_by_id_btn = tk.Button(self.root, text="Далее", command=self.search_func).grid(row=3, column=0, sticky="nw")

    def search_func(self):
        self.db.cursor.execute("SELECT * FROM client WHERE client_id=%s", (self.search_client_by_id_entry.get(),))
        client = self.db.cursor.fetchone()

        self.label1 = tk.Label(self.root, text="ID").grid(row=4, column=0)
        self.label2 = tk.Label(self.root, text="Имя").grid(row=5, column=0)
        self.label3 = tk.Label(self.root, text="Фамилия").grid(row=6, column=0)
        self.label4 = tk.Label(self.root, text="Отчество").grid(row=7, column=0)
        self.label5 = tk.Label(self.root, text="Телефон").grid(row=8, column=0)
        self.label6 = tk.Label(self.root, text="Пароль").grid(row=9, column=0)
        self.label7 = tk.Label(self.root, text="Дата рождения").grid(row=10, column=0)
        
        c = 0
        for i in client:
            self.client_label = tk.Label(self.root, text=f"{i}"+'\n')
            self.client_label.grid(row=4+c, column=1, sticky="nw")
            c += 1

    def back(self):
        self.root.destroy()
        self.root.master.deiconify() 


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

        self.unpaid_orders_btn = tk.Button(self.root,
                                        font=("Arial", 14),
                                        text="Неоплаченные договоры",
                                        command=self.select_unpaid_orders_func)
        self.unpaid_orders_btn.place(x=720, y=100)

        self.update_personal_data_btn = tk.Button(self.root,
                                                  font=("Arial", 14),
                                                  text="Обновить персональные данные",
                                                  command=self.update_personal_data)
        self.update_personal_data_btn.place(x=1000, y=50)

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

        self.db.cursor.execute("""INSERT INTO contract (client_id, space_id, total_coast, contract_status_id)
                               VALUES (%s, %s, %s, %s)
                               RETURNING contract_id""",
                               (self.client_id, space_id, total_coast, 1))
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

    def select_unpaid_orders_func(self):
        UnpaidOrdersWindow(self.root, self.client_id)

    def update_personal_data(self):
        self.update_surname_label = tk.Label(self.root, text="Введите новую фамилию:", font=("Arial", 12), anchor="e", width=30)
        self.update_surname_label.place(x=900, y=90)
        self.update_surname_entry = tk.Entry(self.root)
        self.update_surname_entry.place(x=1200, y=90)

        self.update_name_label = tk.Label(self.root, text="Введите новое имя:", font=("Arial", 12), anchor="e", width=30)
        self.update_name_label.place(x=900, y=130)
        self.update_name_entry = tk.Entry(self.root)
        self.update_name_entry.place(x=1200, y=130)

        self.update_patronymic_label = tk.Label(self.root, text="Введите новое отчество:", font=("Arial", 12), anchor="e", width=30)
        self.update_patronymic_label.place(x=900, y=170)
        self.update_patronymic_entry = tk.Entry(self.root)
        self.update_patronymic_entry.place(x=1200, y=170)

        self.update_phone_label = tk.Label(self.root, text="Введите новый номер телефона:", font=("Arial", 12), anchor="e", width=30)
        self.update_phone_label.place(x=900, y=210)
        self.update_phone_entry = tk.Entry(self.root)
        self.update_phone_entry.place(x=1200, y=210)

        self.update_password_label = tk.Label(self.root, text="Введите новый пароль:", font=("Arial", 12), anchor="e", width=30)
        self.update_password_label.place(x=900, y=250)
        self.update_password_entry = tk.Entry(self.root)
        self.update_password_entry.place(x=1200, y=250)

        self.confirm_update_personal_data_btn = tk.Button(self.root, 
                                                          text="Подтвердить", 
                                                          font=("Arial", 14), 
                                                          command=self.confirm_update_personal_data)
        self.confirm_update_personal_data_btn.place(x=1100, y=290)

    def confirm_update_personal_data(self):
        self.db.cursor.execute("""UPDATE client SET 
                                surname=COALESCE(NULLIF(%s, ''), surname),
                                name_=COALESCE(NULLIF(%s, ''), name_),
                                patronymic=COALESCE(NULLIF(%s, ''), patronymic),
                                phone=COALESCE(NULLIF(%s, ''), phone),
                                password_=COALESCE(NULLIF(%s, ''), password_)
                                WHERE client_id=%s""",
                               (self.update_surname_entry.get(),
                                self.update_name_entry.get(),
                                self.update_patronymic_entry.get(),
                                self.update_phone_entry.get(),
                                self.update_password_entry.get(),
                                self.client_id))
        self.db.connection.commit()

        widgets = ["update_surname_label", "update_surname_entry", "update_name_label", "update_name_entry",
                   "update_patronymic_label", "update_patronymic_entry", "update_phone_label", "update_phone_entry", 
                   "update_password_label", "update_password_entry", "confirm_update_personal_data_btn"
        ]

        for widget_name in widgets:
            if hasattr(self, widget_name):
                widget = getattr(self, widget_name)
                if widget.winfo_exists():
                    widget.destroy()

        self.root.update()

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

    def on_close(self): # не робит
        self.root.destroy()
        self.parent.destroy()

class AllContractsWindow:
    def __init__(self, parent, client_id, coast_per_unit_id):
        self.root = tk.Toplevel(parent)
        self.root.title("Ремонт помещений. Договоры")
        self.root.geometry("800x600")
        
        self.parent = parent
        self.client_id = client_id
        self.coast_per_unit_id = coast_per_unit_id
        self.db = DbConnection()


        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)


        self.back_button = tk.Button(self.main_container, 
                                   text="Назад", 
                                   command=self.back,
                                   font=("Arial", 12))
        self.back_button.pack(anchor="nw", pady=(0, 10))


        self.scroll_frame = tk.Frame(self.main_container)
        self.scroll_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(self.scroll_frame)
        self.scrollbar = tk.Scrollbar(self.scroll_frame, 
                                    orient="vertical", 
                                    command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.content_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.content_frame.bind("<Configure>", 
                             lambda e: self.canvas.configure(
                                 scrollregion=self.canvas.bbox("all")
                             ))
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.load_contracts()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_contracts(self):
        self.db.cursor.execute(
            f"SELECT contract_id FROM contract WHERE client_id={self.client_id}"
        )
        all_contracts = self.db.cursor.fetchall()

        row_counter = 0

        for contract in all_contracts:
            contract_id = contract[0]
            
            contract_frame = tk.LabelFrame(
                self.content_frame,
                text=f"Договор № {contract_id}",
                font=("Arial", 12, "bold"),
                padx=10,
                pady=10
            )
            contract_frame.grid(row=row_counter, column=0, sticky="we", pady=5)
            row_counter += 1

            self.db.cursor.execute(f"""
                SELECT space.street, space.home, space.floor_, space.apartment, space.rooms_num
                FROM space
                JOIN contract ON contract.space_id = space.space_id
                WHERE contract_id={contract_id}
            """)
            space = self.db.cursor.fetchone()
            
            tk.Label(
                contract_frame,
                text=f"Адрес: ул. {space[0]}, д. {space[1]}, эт. {space[2]}, кв. {space[3]}",
                font=("Arial", 11)
            ).grid(row=0, column=0, sticky="w")
            
            tk.Label(
                contract_frame,
                text=f"Комнат: {space[4]}",
                font=("Arial", 11)
            ).grid(row=1, column=0, sticky="w")

            self.db.cursor.execute(
                f"SELECT conclusion_date, completion_date FROM contract WHERE contract_id={contract_id}"
            )
            dates = self.db.cursor.fetchone()
            
            tk.Label(
                contract_frame,
                text=f"Дата заключения: {dates[0]}",
                font=("Arial", 11)
            ).grid(row=2, column=0, sticky="w")
            
            tk.Label(
                contract_frame,
                text=f"Дата окончания: {dates[1]}",
                font=("Arial", 11)
            ).grid(row=3, column=0, sticky="w")

            self.db.cursor.execute(
                f"SELECT total_coast FROM contract WHERE contract_id={contract_id}"
            )
            total_coast = self.db.cursor.fetchone()[0]
            
            self.db.cursor.execute(f"""
                SELECT contract_status.status 
                FROM contract_status
                JOIN contract ON contract.contract_status_id = contract_status.contract_status_id
                WHERE contract_id={contract_id}
            """)
            status = self.db.cursor.fetchone()[0]
            
            tk.Label(
                contract_frame,
                text=f"Общая стоимость: {total_coast} руб.",
                font=("Arial", 11)
            ).grid(row=4, column=0, sticky="w")
            
            tk.Label(
                contract_frame,
                text=f"Статус: {status}",
                font=("Arial", 11)
            ).grid(row=5, column=0, sticky="w")

            self.db.cursor.execute(f"""
                SELECT 
                    servise.servise_name, 
                    works_under_contract.num_of_unit, 
                    works_under_contract.coast_for_work
                FROM works_under_contract
                JOIN contract ON works_under_contract.contract_id = contract.contract_id
                JOIN coast_per_unit ON coast_per_unit.coast_per_unit_id = works_under_contract.coast_per_unit_id
                JOIN servise ON servise.servise_id = coast_per_unit.servise_id
                WHERE contract.contract_id={contract_id}
            """)
            works = self.db.cursor.fetchall()
            
            if works:
                works_label = tk.Label(
                    contract_frame,
                    text="Выполняемые работы:",
                    font=("Arial", 11, "bold")
                )
                works_label.grid(row=6, column=0, sticky="w", pady=(10, 0))
                
                works_table = ttk.Treeview(
                    contract_frame,
                    columns=("service", "quantity", "cost"),
                    show="headings",
                    height=min(len(works), 5)
                )
                works_table.heading("service", text="Услуга")
                works_table.heading("quantity", text="Количество")
                works_table.heading("cost", text="Стоимость")
                
                for work in works:
                    works_table.insert("", "end", values=work)
                
                works_table.grid(row=7, column=0, sticky="we", pady=(0, 10))
                
                works_table.column("service", width=300)
                works_table.column("quantity", width=100, anchor="e")
                works_table.column("cost", width=150, anchor="e")
            self.db.connection.commit()

    def back(self):
        self.root.destroy()
        self.parent.deiconify()

class UnpaidOrdersWindow:
    def __init__(self, parent, client_id):
        self.root = tk.Toplevel(parent)
        self.root.title("Ремонт помещений. Неоплаченные договоры")
        self.root.geometry("1000x600")
        
        self.parent = parent
        self.client_id = client_id
        self.db = DbConnection()

        self.back_button = tk.Button(self.root, 
                                   text="Назад", 
                                   command=self.back,
                                   font=("Arial", 12))
        self.back_button.pack(anchor="nw", pady=(0, 10))

        self.db.cursor.execute(f"SELECT contract_id FROM contract WHERE client_id={self.client_id} AND contract_status_id=1")
        unpaid_orders = self.db.cursor.fetchall()

        if unpaid_orders == []:
            self.no_unpaid_orders_label = tk.Label(self.root,
                                              text="У Вас нет неоплаченных договоров",
                                              font=("Arial", 12))
            self.no_unpaid_orders_label.pack(anchor="nw", pady=(0, 30))
        else:
            cnt = 0

            self.pay_button = tk.Button(self.root, 
                                   text="Оплатить", 
                                   command=self.pay_func,
                                   font=("Arial", 12),
                                   bg="green")
            self.pay_button.pack(anchor="nw", pady=(10, 30))

            self.db.cursor.execute(f"SELECT contract_id FROM contract WHERE contract_status_id=1 AND client_id={self.client_id}")
            unpaid_contracts = self.db.cursor.fetchall()
            for contract in unpaid_contracts:
                self.db.cursor.execute(f"""SELECT contract.contract_id, space.street, space.home, space.floor_,
                                    space.apartment, space.rooms_num, contract.conclusion_date,  contract.total_coast
                                    FROM contract
                                    JOIN space ON contract.space_id = space.space_id
                                    WHERE contract.contract_id={contract[0]}""")
                unpaid_contracts_table = self.db.cursor.fetchall()
                for tuple_unpaid_contract in unpaid_contracts_table:
                    contract_id, street, home, floor_, apartment, rooms_num, conclusion_date, total_coast = tuple_unpaid_contract

                    unpaid_contracts_table_view = ttk.Treeview(self.root,
                                                               columns=("contract_id", "street", "home", "floor_", "apartment", 
                                                                        "rooms_num", "conclusion_date", "total_coast"),
                                                                        show="headings",
                                                                        height=1)
                    unpaid_contracts_table_view.heading("contract_id", text="Номер договора")
                    unpaid_contracts_table_view.heading("street", text="Улица")
                    unpaid_contracts_table_view.heading("home", text="Дом")
                    unpaid_contracts_table_view.heading("floor_", text="Этаж")
                    unpaid_contracts_table_view.heading("apartment", text="Квартира")
                    unpaid_contracts_table_view.heading("rooms_num", text="Количество комнат")
                    unpaid_contracts_table_view.heading("conclusion_date", text="Дата заключения")
                    unpaid_contracts_table_view.heading("total_coast", text="Итоговая стоимость")

                    unpaid_contracts_table_view.insert("", "end", 
                                                       values=(contract_id, street, home, floor_, apartment, rooms_num, conclusion_date, total_coast))
                    unpaid_contracts_table_view.pack(anchor="nw", pady=(0, 30+cnt))

                    unpaid_contracts_table_view.column("contract_id", width=100)
                    unpaid_contracts_table_view.column("street", width=100)
                    unpaid_contracts_table_view.column("home", width=100)
                    unpaid_contracts_table_view.column("floor_", width=100)
                    unpaid_contracts_table_view.column("apartment", width=100)
                    unpaid_contracts_table_view.column("rooms_num", width=150)
                    unpaid_contracts_table_view.column("conclusion_date", width=150)
                    unpaid_contracts_table_view.column("total_coast", width=150)
                    cnt += 10
    
    def pay_func(self):
        pass
        

    def back(self):
        self.root.destroy()
        self.parent.deiconify()

class AllServises(WindowDefaultSize):
    pass

if __name__ == "__main__":
    root = tk.Tk()
    StartWindow(root)
    root.mainloop()