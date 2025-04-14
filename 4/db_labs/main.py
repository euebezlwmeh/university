import tkinter as tk
import re
import psycopg2

WINDOW_DEFAULT_WIDTH = 960
WINDOW_DEFAULT_HEIGHT = 540

class DbConnection:
    def __init__(self):
        try:
            # Установите соединение с базой данных
            self.connection = psycopg2.connect(
                dbname='repair', 
                user='postgres', 
                host='localhost', 
                password='MH0375KCHA8',
                port='5432',  # по умолчанию 5432
                client_encoding='UTF8'
            )

            # Создайте курсор для выполнения операций с базой данных
            self.cursor = self.connection.cursor()

            # Выполните SQL-запрос (например, получить данные из таблицы client)
            # self.cursor.execute("SELECT * FROM client;")
            # self.client_table = self.cursor.fetchall()

            # print(self.client_table)

        except Exception as error:
            print("Error while connecting to PostgreSQL", error)

    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()

class WindowDefaultSize:
    def __init__(self, root):
        self.root = root
        self.root.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}+450+270")
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        if width != WINDOW_DEFAULT_WIDTH or height != WINDOW_DEFAULT_HEIGHT:
            self.root.geometry(f"{WINDOW_DEFAULT_WIDTH}x{WINDOW_DEFAULT_HEIGHT}")

class BackBtn:
    def __init__(self, root, back_command):
        self.root = root
        self.create_back_btn(self.root, back_command)

    def create_back_btn(self, root, back_command): 
        self.back_btn = tk.Button(root, text="Назад", width=6, height=1, font=("Arial", 12), command=back_command)
        self.back_btn.place(x=10, y=10)

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

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

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

        self.sign_in_btn = tk.Button(self.root, text="Войти", width=14, height=1, font=("Arial", 12), command=self.sign_in)
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
                "SELECT phone, password_ FROM client WHERE phone = %s AND password_ = %s", (phone, password))
            
            result = self.db.cursor.fetchone()
            
            if result:
                MainWindow(self.root)
                self.root.withdraw()
            else:
                self.error_label = tk.Label(self.root, bg="red", font=("Arial", 12), text="Ошибка: Неверно введены данные!")
                self.error_label.place(x=380, y=360)
        
        except Exception as e:
            print("Ошибка при выполнении запроса:", e)

class MainWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.root = tk.Toplevel(parent)
        self.root.title("Ремонт помещений")
        super().__init__(self.root)

        BackBtn(self.root, self.back)
        self.parent = parent

        self.db = DbConnection()

        self.add_order_btn = tk.Button(self.root, 
                                       font=("Arial", 14), 
                                       text="Создать заказ", 
                                       command=self.add_order_func)
        self.add_order_btn.place(x=220, y=100)

    def add_order_func(self):
        self.add_servise_btn = tk.Button(self.root,
                                     font=("Arial", 14),
                                     text="Добавить услугу",
                                     command=self.add_servise_func)
        self.add_servise_btn.place(x=220, y=150)
        
    def add_servise_func(self):
        surfaces_arr = []

        try:
            self.db.cursor.execute(
                "SELECT surface_name FROM surface"
            )
            for row in self.db.cursor:
                surfaces_arr.append(row)
            
            print(surfaces_arr)
        except:
            print("ошибка")

    def back(self):
        self.root.destroy()
        self.root.master.deiconify()

    def on_close(self):  # не работает как надо
        self.root.destroy()
        self.parent.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    # DbConnection()
    StartWindow(root)
    root.mainloop()
