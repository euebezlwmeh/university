from tkinter import *
from tkinter import ttk
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel 

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.model = TableModel()
        self.table = TableCanvas(self, model=self.model)
        self.table.createTableFrame()
        root.bind('<ButtonRelease-1>', self.clicked)

        # Добавим тестовые данные, если файл не найден
        self.create_widgets()

    def create_widgets(self):
        # Проверяем, есть ли файл, если нет - создаем тестовые данные
        try:
            self.table.model.load('save.table')
        except FileNotFoundError:
            # Создаем тестовые данные
            data = {
                'rec1': {'col1': 1, 'col2': 'A'},
                'rec2': {'col1': 2, 'col2': 'B'},
                'rec3': {'col1': 3, 'col2': 'C'}
            }
            self.table.model.importDict(data)
            print("Created sample data as 'save.table' not found")

        self.table.redrawTable()

    def clicked(self, event):
        try:
            rclicked = self.table.get_row_clicked(event)
            cclicked = self.table.get_col_clicked(event)
            clicks = (rclicked, cclicked)
            print('clicks:', clicks)
            
            if clicks:
                try: 
                    print('single cell:', self.table.model.getValueAt(clicks[0], clicks[1]))
                except: 
                    print('No record at:', clicks)

                try: 
                    print('entire record:', self.table.model.getRecordAtRow(clicks[0]))
                except: 
                    print('No record at:', clicks)
        except Exception as e: 
            print('Error:', e)

root = Tk()
root.title('Table Test')
app = Application(master=root)
print('Starting mainloop()')
app.mainloop()