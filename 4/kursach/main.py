import customtkinter as ctk
import psycopg2

DEFAULT_COLOR = "#2262b3"

class DbConnection:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                dbname='postgres', 
                user='postgres', 
                host='localhost', 
                password='MH0375KCHA8',
                port='5432',
                client_encoding='win1251'
            )
            self.cursor = self.connection.cursor()
        except Exception as error:
            print("Error while connecting to PostgreSQL", error)

    def __del__(self):
        if hasattr(self, 'connection'):
            self.connection.close()

class WindowDefaultSettings:
    def __init__(self, parent):
        self.parent = parent
        self.app = ctk.CTkToplevel(parent)
        self.app.geometry("1000x550")
        ctk.set_appearance_mode("light")
        self.db = DbConnection()
        self.app.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.parent.deiconify()
        self.app.destroy()

class MainWindow:
    def __init__(self, app):
        self.app = app
        self.app.title("Медицинский центр. Главная")
        self.app.geometry("1000x550")
        ctk.set_appearance_mode("light")
        
        self.addMedicineBtn = ctk.CTkButton(self.app, 
                                       text="Добавить препарат",
                                       fg_color=DEFAULT_COLOR,  
                                       command=self.addMedicineFunc)
        self.addMedicineBtn.grid(row=0, column=0, padx=20, pady=20, ipadx=20, ipady=20)

        self.addMedicineBatchBtn = ctk.CTkButton(self.app, 
                                       text="Добавить партию препарата",
                                       fg_color=DEFAULT_COLOR,  
                                       command=self.addMedicineBatchFunc)
        self.addMedicineBatchBtn.grid(row=1, column=0, padx=20, pady=20, ipadx=20, ipady=20)

    def addMedicineFunc(self):
        self.app.withdraw()
        AddMedicineWindow(self.app)

    def addMedicineBatchFunc(self):
        self.app.withdraw()
        AddMedicineBatchWindow(self.app)

class AddMedicineWindow(WindowDefaultSettings):
    def __init__(self, parent):
        super().__init__(parent)
        self.app.title("Медицинский центр. Добавить препарат")

        self.DosageLabel = ctk.CTkLabel(self.app, text="Введите МНН:")
        self.DosageLabel.grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.InnEntry = ctk.CTkEntry(self.app)
        self.InnEntry.grid(row=0, column=1, padx=8, pady=8)

        self.TradeNameLabel = ctk.CTkLabel(self.app, text="Введите торговое\n название:")
        self.TradeNameLabel.grid(row=1, column=0, padx=8, pady=8, sticky="e")
        self.TradeNameEntry = ctk.CTkEntry(self.app)
        self.TradeNameEntry.grid(row=1, column=1, padx=8, pady=8)

        controlLevelArr = ["Общий", "Психотропный", "Наркотический"]

        self.controlLevelLabel = ctk.CTkLabel(self.app, text="Введите уровень\n контроля:")
        self.controlLevelLabel.grid(row=2, column=0, padx=8, pady=8, sticky="e")
        self.controlLevelMenu = ctk.CTkOptionMenu(self.app, values=controlLevelArr)
        self.controlLevelMenu.grid(row=2, column=1, padx=8, pady=8)

        formReleaseArr = ["Таблетки", "Гранулы", "Порошки", "Пилюли", "Мазь", "Раствор", "Настойка", "Микстура", "Капли"]

        self.FormReleaseLabel = ctk.CTkLabel(self.app, text="Введите форму выпуска:")
        self.FormReleaseLabel.grid(row=3, column=0, padx=8, pady=8, sticky="e")
        self.FormReleaseMenu = ctk.CTkOptionMenu(self.app, values=formReleaseArr)
        self.FormReleaseMenu.grid(row=3, column=1, padx=8, pady=8)

        self.DosageLabel = ctk.CTkLabel(self.app, text="Введите дозировку:")
        self.DosageLabel.grid(row=4, column=0, padx=8, pady=8, sticky="e")
        self.DosageEntry = ctk.CTkEntry(self.app)
        self.DosageEntry.grid(row=4, column=1, padx=8, pady=8)

        self.MinTemperatureLabel = ctk.CTkLabel(self.app, text="Введите минимальную\n температуру хранения:")
        self.MinTemperatureLabel.grid(row=5, column=0, padx=8, pady=8, sticky="e")
        self.MinTemperatureEntry = ctk.CTkEntry(self.app)
        self.MinTemperatureEntry.grid(row=5, column=1, padx=8, pady=8)

        self.MaxTemperatureLabel = ctk.CTkLabel(self.app, text="Введите максимальную\n температуру хранения:")
        self.MaxTemperatureLabel.grid(row=6, column=0, padx=8, pady=8, sticky="e")
        self.MaxTemperatureEntry = ctk.CTkEntry(self.app)
        self.MaxTemperatureEntry.grid(row=6, column=1, padx=8, pady=8)

        lightingArr = ["Тёмное", "Ограниченное", "Не чувствителен", "Требуется"]

        self.LightingLabel = ctk.CTkLabel(self.app, text="Введите необходимое\n освещение:")
        self.LightingLabel.grid(row=7, column=0, padx=8, pady=8, sticky="e")
        self.LightingMenu = ctk.CTkOptionMenu(self.app, values=lightingArr)
        self.LightingMenu.grid(row=7, column=1, padx=8, pady=8)

        self.HumidityLabel = ctk.CTkLabel(self.app, text="Введите влажность\n хранения:")
        self.HumidityLabel.grid(row=8, column=0, padx=8, pady=8, sticky="e")
        self.HumidityEntry = ctk.CTkEntry(self.app)
        self.HumidityEntry.grid(row=8, column=1, padx=8, pady=8)

        self.confirmAddMedicineBtn = ctk.CTkButton(self.app, 
                                               text="Подтвердить", 
                                               fg_color=DEFAULT_COLOR, 
                                               command=self.confirmAddMedicineFunc)
        self.confirmAddMedicineBtn.grid(row=9, column=1, padx=8, pady=8)

    def confirmAddMedicineFunc(self):
        self.db.cursor.execute("""INSERT INTO Storage_conditions (min_temperature, max_temperature, lighting, humidity) 
                               VALUES (%s, %s, %s, %s)
                               RETURNING id_storage_conditions""", 
                               (self.MinTemperatureEntry.get(), self.MaxTemperatureEntry.get(), 
                               self.LightingMenu.get(), self.HumidityEntry.get()))
        id_storage_conditions = self.db.cursor.fetchone()[0]
        self.db.connection.commit()

        self.db.cursor.execute("""INSERT INTO Medicine (id_storage_conditions, INN, trade_name, control_level, form_release, dosage)
                               VALUES (%s, %s, %s, %s, %s, %s)""", 
                               (id_storage_conditions, self.InnEntry.get(), 
                               self.TradeNameEntry.get(), self.controlLevelMenu.get(),
                               self.FormReleaseMenu.get(), self.DosageEntry.get()))
        self.db.connection.commit()

        SuccessWindow(self.app)
        self.app.destroy()

class AddMedicineBatchWindow(WindowDefaultSettings):
    def __init__(self, parent):
        super().__init__(parent)
        self.app.title("Медицинский центр. Добавить партию препарата")

        self.ChooseProducerButton = ctk.CTkButton(self.app, 
                                              text="Выбрать производителя", 
                                              fg_color=DEFAULT_COLOR, 
                                              command=self.ChooseProducerFunc)
        self.ChooseProducerButton.grid(row=0, column=0, padx=20, pady=20, ipadx=20, ipady=20)

        self.OrLabel = ctk.CTkLabel(self.app, text="Или")
        self.OrLabel.grid(row=0, column=1, padx=20, pady=5)

        self.AddProducerButton = ctk.CTkButton(self.app, 
                                           text="Добавить производителя", 
                                           fg_color=DEFAULT_COLOR, 
                                           command=self.AddProducerFunc)
        self.AddProducerButton.grid(row=0, column=2, padx=20, pady=20, ipadx=20, ipady=20)

    def ChooseProducerFunc(self):
        ChooseProducerWindow(self.app)
        self.app.withdraw()

    def AddProducerFunc(self):
        AddProducerWindow(self.app)
        self.app.withdraw()

class ChooseProducerWindow(WindowDefaultSettings):
    def __init__(self, parent):
        super().__init__(parent)
        self.app.title("Выбор производителя")

class AddProducerWindow(WindowDefaultSettings):
    def __init__(self, parent):
        super().__init__(parent)
        self.app.title("Добавление производителя")

        self.ProducerNameLabel = ctk.CTkLabel(self.app, text="Добавить название производителя")
        self.ProducerNameLabel.grid(row=0, column=0, ipadx=8, ipady=8, sticky="e")
        self.ProducerNameEntry = ctk.CTkEntry(self.app)
        self.ProducerNameEntry.grid(row=0, column=1, ipadx=8, ipady=8, sticky="e")

        self.ProducerCountryLabel = ctk.CTkLabel(self.app, text="Добавить страну производителя")
        self.ProducerCountryLabel.grid(row=1, column=0, ipadx=8, ipady=8, sticky="e")
        self.ProducerCountryEntry = ctk.CTkEntry(self.app)
        self.ProducerCountryEntry.grid(row=1, column=1, ipadx=8, ipady=8, sticky="e")

        self.ProducerContactsLabel = ctk.CTkLabel(self.app, text="Добавить контакты производителя")
        self.ProducerContactsLabel.grid(row=2, column=0, ipadx=8, ipady=8, sticky="e")
        self.ProducerContactsEntry = ctk.CTkEntry(self.app)
        self.ProducerContactsEntry.grid(row=2, column=1, ipadx=8, ipady=8, sticky="e")

        self.AddProducerButton = ctk.CTkButton(self.app, text="Добавить производителя", fg_color=DEFAULT_COLOR, command=self.AddProducerFunc)
        self.AddProducerButton.grid(row=3, column=0, ipadx=8, ipady=8, sticky="e")

    def AddProducerFunc(self):
        self.parent.deiconify()
        self.app.destroy()

class SuccessWindow:
    def __init__(self, parent):
        self.parent = parent
        self.app = ctk.CTkToplevel(parent)
        self.app.title("Успешно!")
        self.app.geometry("300x150")

        self.SuccessLabel = ctk.CTkLabel(self.app, text="Успешно!", bg_color="#61c671")
        self.SuccessLabel.pack(pady=40)

        self.app.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.app.destroy()

if __name__ == "__main__":
    app = ctk.CTk()
    main_window = MainWindow(app)
    app.mainloop()