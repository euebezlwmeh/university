import customtkinter as ctk
from tkinter import messagebox
from CTkTable import *
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
        self.app.geometry("1000x650")
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

        self.app.grid_columnconfigure(0, weight=1)
        
        self.addMedicineBtn = ctk.CTkButton(self.app, 
                                       text="Добавить препарат",
                                       fg_color=DEFAULT_COLOR,  
                                       command=self.addMedicineFunc)
        self.addMedicineBtn.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        self.addMedicineBatchBtn = ctk.CTkButton(self.app, 
                                       text="Добавить партию препарата",
                                       fg_color=DEFAULT_COLOR,  
                                       command=self.addMedicineBatchFunc)
        self.addMedicineBatchBtn.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.BatchWritingOffBtn = ctk.CTkButton(self.app,
                                                text="Списать препараты из партии",
                                                fg_color=DEFAULT_COLOR,
                                                command=self.BatchWritingOffFunc)
        self.BatchWritingOffBtn.grid(row=2, column=0, padx=20, pady=5, sticky="w")

    def addMedicineFunc(self):
        self.app.withdraw()
        AddMedicineWindow(self.app)

    def addMedicineBatchFunc(self):
        self.app.withdraw()
        AddMedicineBatchWindow(self.app)

    def BatchWritingOffFunc(self):
        self.app.withdraw()
        BatchWritingOffWindow(self.app)

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

        messagebox.showinfo(title="Успех", message="Препарат успешно добавлен!")
        self.parent.deiconify()
        self.app.destroy()

class AddMedicineBatchWindow(WindowDefaultSettings):
    def __init__(self, parent):
        super().__init__(parent)
        self.app.title("Медицинский центр. Добавить партию препарата")

        self.app.grid_columnconfigure(0, weight=1)

        self.ChooseProducerButton = ctk.CTkButton(self.app, 
                                              text="Выбрать производителя", 
                                              fg_color=DEFAULT_COLOR,
                                              command=self.ChooseProducerFunc)
        self.ChooseProducerButton.grid(row=0, column=0, padx=20, pady=5, sticky="w")

        self.OrLabel = ctk.CTkLabel(self.app, text="Или")
        self.OrLabel.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        self.AddProducerButton = ctk.CTkButton(self.app, 
                                           text="Добавить производителя", 
                                           fg_color=DEFAULT_COLOR,
                                           command=self.AddProducerFunc)
        self.AddProducerButton.grid(row=2, column=0, padx=20, pady=5, sticky="w")

        self.SelectProducerLabelText = "Выберите производителя"
        self.SelectProducerLabel = ctk.CTkLabel(self.app, text=f"Производитель: {self.SelectProducerLabelText}")
        self.SelectProducerLabel.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        self.ChooseMedicineButton = ctk.CTkButton(self.app,
                                                text="Выбрать препарат", 
                                                fg_color=DEFAULT_COLOR,
                                                command=self.ChooseMedicineFunc)
        self.ChooseMedicineButton.grid(row=4, column=0, padx=20, pady=5, sticky="w")

        self.SelectMedicineLabelText = "Выберите препарат"
        self.SelectMedicineLabel = ctk.CTkLabel(self.app, text=f"Препарат: {self.SelectMedicineLabelText}")
        self.SelectMedicineLabel.grid(row=5, column=0, padx=20, pady=5, sticky="w")

        self.SeriesLabel = ctk.CTkLabel(self.app, text="Введите серию препарата:")
        self.SeriesLabel.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        self.SeriesEntry = ctk.CTkEntry(self.app)
        self.SeriesEntry.grid(row=7, column=0, padx=20, pady=5, sticky="w")

        self.ProductionDateLabel = ctk.CTkLabel(self.app, text="Введите дату производитва:")
        self.ProductionDateLabel.grid(row=8, column=0, padx=20, pady=5, sticky="w")
        self.ProductionDateEntry = ctk.CTkEntry(self.app)
        self.ProductionDateEntry.grid(row=9, column=0, padx=20, pady=5, sticky="w")

        self.ExpirationDateLabel = ctk.CTkLabel(self.app, text="Введите срок годности:")
        self.ExpirationDateLabel.grid(row=10, column=0, padx=20, pady=5, sticky="w")
        self.ExpirationDateEntry = ctk.CTkEntry(self.app)
        self.ExpirationDateEntry.grid(row=11, column=0, padx=20, pady=5, sticky="w")

        self.CountLabel = ctk.CTkLabel(self.app, text="Введите количество препарата в серии:")
        self.CountLabel.grid(row=12, column=0, padx=20, pady=5, sticky="w")
        self.CountEntry = ctk.CTkEntry(self.app)
        self.CountEntry.grid(row=13, column=0, padx=20, pady=5, sticky="w")

        self.AddMedicineBatchButton = ctk.CTkButton(self.app, 
                                                    text="Добавить партию", 
                                                    fg_color=DEFAULT_COLOR,
                                                    command=self.AddMedicineBatchFunc)
        self.AddMedicineBatchButton.grid(row=14, column=0, padx=20, pady=5, sticky="w")

    def ChooseProducerFunc(self):
        chooserWindow = ChooseProducerWindow(self.app)
        self.app.withdraw()
        self.app.wait_window(chooserWindow.app)
        if chooserWindow.selected_producer:
            self.producer = chooserWindow.selected_producer
            self.SelectProducerLabelText = f"Производитель: Название - {self.producer[1]}, Страна - {self.producer[2]}, Контакты - {self.producer[3]}"
            self.SelectProducerLabel.configure(text=self.SelectProducerLabelText)

    def AddProducerFunc(self):
        addWindow = AddProducerWindow(self.app)
        self.app.withdraw()
        self.app.wait_window(addWindow.app)
        if addWindow.added_producer:
            self.db.cursor.execute("SELECT * FROM producer WHERE id_producer=%s", addWindow.added_producer)
            self.producer = self.db.cursor.fetchone()
            self.SelectProducerLabelText = f"Производитель: Название - {self.producer[1]}, Страна - {self.producer[2]}, Контакты - {self.producer[3]}"
            self.SelectProducerLabel.configure(text=self.SelectProducerLabelText)

    def ChooseMedicineFunc(self):
        medicineWindow = ChooseMedicineWindow(self.app)
        self.app.withdraw()
        self.app.wait_window(medicineWindow.app)
        if medicineWindow.selected_medicine:
            self.medicine = medicineWindow.selected_medicine
            self.SelectMedicineLabelText = f"Препарат: МНН - {self.medicine[2]}, Торговое название - {self.medicine[3]}, Уровень контроля - {self.medicine[4]}, Форма выпуска: {self.medicine[5]}, Дозировка - {self.medicine[6]}"
            self.SelectMedicineLabel.configure(text=self.SelectMedicineLabelText)

    def AddMedicineBatchFunc(self):
        self.db.cursor.execute("""INSERT INTO Medicine_batch (id_medicine, id_producer, series, production_date, expiration_date, count)
                                VALUES (%s, %s, %s, %s, %s, %s)""", 
                                (self.medicine[0], self.producer[0],
                                 self.SeriesEntry.get(), self.ProductionDateEntry.get(),
                                 self.ExpirationDateEntry.get(), self.CountEntry.get()))
        self.db.connection.commit()
        messagebox.showinfo(title="Успех", message="Партия успешно добавлена!")
        self.parent.deiconify()
        self.app.destroy()

class ChooseProducerWindow(WindowDefaultSettings):
    def __init__(self, parent):
        super().__init__(parent)
        self.app.title("Выбор производителя")

        self.db.cursor.execute("SELECT * FROM Producer")
        self.producers_data = self.db.cursor.fetchall()

        main_frame = ctk.CTkFrame(self.app)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        scroll_frame = ctk.CTkScrollableFrame(main_frame)
        scroll_frame.pack(fill="both", expand=True)

        headers_frame = ctk.CTkFrame(scroll_frame)
        headers_frame.pack(fill="x")
        
        ctk.CTkLabel(headers_frame, text="Название", width=200, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="Страна", width=150, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="Контакты", width=300, anchor="w").pack(side="left", padx=5)

        self.producer_frames = []
        for i, producer in enumerate(self.producers_data):
            frame = ctk.CTkFrame(scroll_frame)
            frame.pack(fill="x", pady=2)

            ctk.CTkLabel(frame, text=producer[1], width=200, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=producer[2], width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=producer[3], width=300, anchor="w").pack(side="left", padx=5)

            frame.bind("<Button-1>", lambda e, idx=i: self._on_row_click(idx))
            for child in frame.winfo_children():
                child.bind("<Button-1>", lambda e, idx=i: self._on_row_click(idx))
            
            self.producer_frames.append(frame)

        select_button = ctk.CTkButton(
            main_frame,
            text="Выбрать",
            command=self._on_select,
            fg_color=DEFAULT_COLOR,
            height=40,
            font=("Arial", 14)
        )
        select_button.pack(pady=10)
        
        self.selected_index = None
    
    def _on_row_click(self, index):
        for i, frame in enumerate(self.producer_frames):
            frame.configure(fg_color="transparent")

        self.producer_frames[index].configure(fg_color="#1F6AA5")
        self.selected_index = index
    
    def _on_select(self):
        if self.selected_index is None:
            messagebox.showwarning("Выбор", "Пожалуйста, выберите производителя из списка")
            return 
        try:
            self.selected_producer = self.producers_data[self.selected_index]
            self.parent.deiconify()
            self.app.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при выборе: {str(e)}")

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
        self.db.cursor.execute("""INSERT INTO Producer(name_, country, contacts)
                        VALUES (%s, %s, %s) RETURNING id_producer""", 
                        (self.ProducerNameEntry.get(), self.ProducerCountryEntry.get(), self.ProducerContactsEntry.get()))
        self.added_producer = self.db.cursor.fetchone()
        self.db.connection.commit()
        self.parent.deiconify()
        self.app.destroy()

class ChooseMedicineWindow(WindowDefaultSettings):
    def __init__(self, parent):
        super().__init__(parent)
        self.app.title("Медицинский центр. Выбор препарата")

        self.db.cursor.execute("SELECT * FROM medicine")
        self.AllMedicines = self.db.cursor.fetchall()

        main_frame = ctk.CTkFrame(self.app)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        scroll_frame = ctk.CTkScrollableFrame(main_frame)
        scroll_frame.pack(fill="both", expand=True)

        headers_frame = ctk.CTkFrame(scroll_frame)
        headers_frame.pack(fill="x")
        
        ctk.CTkLabel(headers_frame, text="МНН", width=350, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="Торговое название", width=150, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="Уровень контроля", width=150, anchor="w").pack(side="left", padx=5)
        ctk.CTkLabel(headers_frame, text="Форма выпуска", width=150, anchor="w").pack(side="left", padx=5)  
        ctk.CTkLabel(headers_frame, text="Дозировка", width=150, anchor="w").pack(side="left", padx=5)

        self.medicine_frames = []
        for i, medicine in enumerate(self.AllMedicines):
            frame = ctk.CTkFrame(scroll_frame)
            frame.pack(fill="x", pady=2)

            ctk.CTkLabel(frame, text=medicine[2], width=350, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=medicine[3], width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=medicine[4], width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=medicine[5], width=150, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=medicine[6], width=150, anchor="w").pack(side="left", padx=5)

            frame.bind("<Button-1>", lambda e, idx=i: self._on_row_click(idx))
            for child in frame.winfo_children():
                child.bind("<Button-1>", lambda e, idx=i: self._on_row_click(idx))
            
            self.medicine_frames.append(frame)

        select_button = ctk.CTkButton(
            main_frame,
            text="Выбрать",
            command=self._on_select,
            fg_color=DEFAULT_COLOR,
            height=40,
            font=("Arial", 14)
        )
        select_button.pack(pady=10)
        
        self.selected_index = None

    def _on_row_click(self, index):
        for i, frame in enumerate(self.medicine_frames):
            frame.configure(fg_color="transparent")

        self.medicine_frames[index].configure(fg_color="#1F6AA5")
        self.selected_index = index

    def _on_select(self):
        if self.selected_index is None:
            messagebox.showwarning("Выбор", "Пожалуйста, выберите препарат из списка")
            return 
        try:
            self.selected_medicine = self.AllMedicines[self.selected_index]
            self.parent.deiconify()
            self.app.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при выборе: {str(e)}")

class BatchWritingOffWindow(WindowDefaultSettings):
    def __init__(self, parent):
        super().__init__(parent)

        self.app.grid_columnconfigure(0, weight=1)

        self.app.title("Медицинский центр. Списание препаратов из партии")

        self.BatchWritingOffButton = ctk.CTkButton(self.app,
                                                text="Выбрать партию препарата",
                                                fg_color=DEFAULT_COLOR,  
                                                command=self.ChooseMedicineBatchFunc)
        self.BatchWritingOffButton.grid(row=0, column=0, padx=20, pady=5, sticky="w")
        self.SelectMedicineBatchLabel = ctk.CTkLabel(self.app, text="Партия препарата: выберите партию")
        self.SelectMedicineBatchLabel.grid(row=1, column=0, padx=20, pady=5, sticky="w")

        BatchWritingOffReasons = ["Истёкший срок годности", "Повреждение упаковки",
                                 "Изменение физико-химических свойств", "Брак производства", 
                                 "Нарушение условий хранения", "Механическое повреждение",
                                 "Нарушение герметичности"]
        self.BatchWritingOffReasonLabel = ctk.CTkLabel(self.app, text="Выберите причину списания:")
        self.BatchWritingOffReasonLabel.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.BatchWritingOffReasonMenu = ctk.CTkOptionMenu(self.app,values=BatchWritingOffReasons)
        self.BatchWritingOffReasonMenu.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        self.CountWritingOffMedicineLabel = ctk.CTkLabel(self.app, text="Введите количество списанных препаратов:")
        self.CountWritingOffMedicineLabel.grid(row=4, column=0, padx=20, pady=5, sticky="w")

        self.CountWritingOffMedicineEntry = ctk.CTkEntry(self.app)
        self.CountWritingOffMedicineEntry.grid(row=5, column=0, padx=20, pady=5, sticky="w")

        self.WritingOffAgreeButton = ctk.CTkButton(self.app, text="Списать препараты", command=self.WritingOffFunc)
        self.WritingOffAgreeButton.grid(row=6, column=0, padx=20, pady=5, sticky="w")

    def ChooseMedicineBatchFunc(self):
        chooserWindow = ChooseMedicineBatchWindow(self.app)
        self.app.withdraw()
        self.app.wait_window(chooserWindow.app)
        if chooserWindow.selected_medicine_batch:
            self.medicine_batch = chooserWindow.selected_medicine_batch
            self.SelectMedicineBatchLabelText = f"""Партия: МНН - {self.medicine_batch[1]}, Торговое название - {self.medicine_batch[2]}, Уровень контроля - {self.medicine_batch[3]}\n
                                                    Форма выпуска - {self.medicine_batch[4]}, Дозировка - {self.medicine_batch[5]}, Серия - {self.medicine_batch[6]}\n
                                                    Дата производитва - {self.medicine_batch[7]}, Срок годности - {self.medicine_batch[8]}, Количество - {self.medicine_batch[9]}\n"""
            self.SelectMedicineBatchLabel.configure(text=self.SelectMedicineBatchLabelText)

    def WritingOffFunc(self):
        count_to_write_off = int(self.CountWritingOffMedicineEntry.get())
        current_count = int(self.medicine_batch[9])

        if count_to_write_off <= 0:
            messagebox.showerror("Ошибка", "Количество для списания должно быть положительным числом")
            return
            
        if count_to_write_off > current_count:
            messagebox.showerror("Ошибка", "Нельзя списать больше препаратов, чем есть в партии")
            return

        self.db.cursor.execute("BEGIN")

        self.db.cursor.execute("""
            INSERT INTO Batch_writing_off (id_medicine_batch, written_off_date, reason, count)
            VALUES (%s, CURRENT_DATE, %s, %s)
            RETURNING id_batch_writing_off
        """, (
            self.medicine_batch[0], 
            self.BatchWritingOffReasonMenu.get(), 
            count_to_write_off
        ))

        self.db.cursor.execute("""
            UPDATE Medicine_batch 
            SET count = count - %s
            WHERE id_medicine_batch = %s
        """, (count_to_write_off, self.medicine_batch[0]))

        self.db.connection.commit()
        
        messagebox.showinfo("Успех", "Препараты успешно списаны")

        self.medicine_batch = list(self.medicine_batch)
        self.medicine_batch[9] = current_count - count_to_write_off
        self.parent.deiconify()
        self.app.destroy()

class ChooseMedicineBatchWindow(WindowDefaultSettings):
    def __init__(self, parent):
        super().__init__(parent)
        self.app.title("Выбор партии препарата")
        
        self.db.cursor.execute("""SELECT Medicine_batch.id_medicine_batch, Medicine.INN, Medicine.trade_name, 
                               Medicine.control_level, Medicine.form_release, Medicine.dosage, 
                               Medicine_batch.series, Medicine_batch.production_date, 
                               Medicine_batch.expiration_date, Medicine_batch.count 
                               FROM Medicine_batch
                               JOIN Medicine ON Medicine.id_medicine = Medicine_batch.id_medicine""")
        self.AllMedicineBatches = self.db.cursor.fetchall()

        main_container = ctk.CTkFrame(self.app)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.canvas = ctk.CTkCanvas(main_container)
        self.canvas.pack(side="left", fill="both", expand=True)

        v_scrollbar = ctk.CTkScrollbar(main_container, orientation="vertical", command=self.canvas.yview)
        v_scrollbar.pack(side="right", fill="y")

        h_scrollbar = ctk.CTkScrollbar(self.app, orientation="horizontal", command=self.canvas.xview)
        h_scrollbar.pack(side="bottom", fill="x")

        self.canvas.configure(
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        headers_frame = ctk.CTkFrame(self.scrollable_frame)
        headers_frame.pack(fill="x")

        column_widths = [300, 150, 150, 150, 150, 150, 150, 150, 150]
        headers = ["МНН", "Торговое название", "Уровень контроля", "Форма выпуска", 
                 "Дозировка", "Серия", "Дата производства", "Срок годности", "Количество"]
        
        for header, width in zip(headers, column_widths):
            ctk.CTkLabel(headers_frame, text=header, width=width, anchor="w").pack(side="left", padx=5)

        self.medicine_batches_frames = []
        for i, medicine_batch in enumerate(self.AllMedicineBatches):
            frame = ctk.CTkFrame(self.scrollable_frame)
            frame.pack(fill="x", pady=2)
            
            for col, (value, width) in enumerate(zip(medicine_batch[1:], column_widths)):
                ctk.CTkLabel(frame, text=str(value), width=width, anchor="w").pack(side="left", padx=5)

            frame.bind("<Button-1>", lambda e, idx=i: self._on_row_click(idx))
            for child in frame.winfo_children():
                child.bind("<Button-1>", lambda e, idx=i: self._on_row_click(idx))
            
            self.medicine_batches_frames.append(frame)

        select_button = ctk.CTkButton(
            self.scrollable_frame,
            text="Выбрать",
            command=self._on_select,
            fg_color=DEFAULT_COLOR,
            height=40,
            font=("Arial", 14)
        )
        select_button.pack(pady=10)

        self.scrollable_frame.bind("<Enter>", self._bind_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_mousewheel)
        
        self.selected_index = None
    
    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
    
    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_row_click(self, index):
        for i, frame in enumerate(self.medicine_batches_frames):
            frame.configure(fg_color="transparent")

        self.medicine_batches_frames[index].configure(fg_color="#1F6AA5")
        self.selected_index = index
    
    def _on_select(self):
        if self.selected_index is None:
            messagebox.showwarning("Выбор", "Пожалуйста, выберите партию препарата из списка")
            return 
        try:
            self.selected_medicine_batch = self.AllMedicineBatches[self.selected_index]
            self.parent.deiconify()
            self.app.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при выборе: {str(e)}")

if __name__ == "__main__":
    app = ctk.CTk()
    main_window = MainWindow(app)
    app.mainloop()