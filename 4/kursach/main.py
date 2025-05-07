import customtkinter as ctk
import psycopg2

class WindowDefaultSize:
    def __init__(self, app):
        self.app = app
        app.geometry("900x450")


class MainWindow(WindowDefaultSize):
    def __init__(self, app):
        super().__init__(app)
        
        self.app.title("Медицинский центр. Главная")

        self.addMedicineBtn = ctk.CTkButton(self.app, 
                                       text="Добавить препарат",
                                       bg_color="#5eb481",  
                                       command=self.addMedicineFunc)
        self.addMedicineBtn.pack(anchor="nw", padx=20, pady=20)

    def addMedicineFunc(self):
        addMedicineWindow(self.app)
        self.app.withdraw()

class addMedicineWindow(WindowDefaultSize):
    def __init__(self, parent):
        self.parent = parent
        self.app = ctk.CTkToplevel(parent)
        super().__init__(self.app)

        self.app.title("Добавить препарат")

        self.DosageLabel = ctk.CTkLabel(self.app, text="Введите МНН", justify="right")
        self.DosageLabel.grid(row=0, column=0, ipadx=8, ipady=8)
        self.InnEntry = ctk.CTkEntry(self.app)
        self.InnEntry.grid(row=0, column=1, ipadx=8, ipady=8)

        self.TradeNameLabel = ctk.CTkLabel(self.app, text="Введите торговое название", justify="right")
        self.TradeNameLabel.grid(row=1, column=0, ipadx=8, ipady=8)
        self.TradeNameEntry = ctk.CTkEntry(self.app)
        self.TradeNameEntry.grid(row=1, column=1, ipadx=8, ipady=8)

        formReleaseArr = ["Таблетки", "Гранулы", "Порошки", "Пилюли", "Мазь", "Раствор", "Настойка", "Микстура", "Капли"]

        self.FormReleaseLabel = ctk.CTkLabel(self.app, text="Введите форму выпуска", justify="right")
        self.FormReleaseLabel.grid(row=2, column=0, ipadx=8, ipady=8)
        self.FormReleaseMenu = ctk.CTkOptionMenu(self.app, 
                                                 values=formReleaseArr)
        self.FormReleaseMenu.grid(row=2, column=1, ipadx=8, ipady=8)

        self.DosageLabel = ctk.CTkLabel(self.app, text="Введите дозировку", justify="right")
        self.DosageLabel.grid(row=3, column=0, ipadx=8, ipady=8)
        self.DosageEntry = ctk.CTkEntry(self.app)
        self.DosageEntry.grid(row=3, column=1, ipadx=8, ipady=8)

        

        self.app.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.parent.deiconify()
        self.app.destroy()
        
if __name__ == "__main__":
    app = ctk.CTk()
    MainWindow(app)
    app.mainloop()