from folder import electrodevices, docx_save
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown 
from abc import ABC, abstractmethod

class Calculator(ABC): 
    @abstractmethod
    def calculate(self, instance):  
        pass

class myApp(App, Calculator):

    def __str__(self): 
        return f"Электроприбор: {self.electrodevice_button.text}"

    def __repr__(self):
        return f"(electrodevice={self.electrodevice_button.text})"

    def build(self):
        layout = GridLayout(cols=2, row_force_default = True, row_default_height = 30)

        electrodevice_label = Label(text="Бытовая техника: ")
        self.electrodevice_dropdown = DropDown()
        self.electrodevice_button = Button(text=f'{electrodevices.iron.name}')
        self.electrodevice_button.bind(on_release=self.electrodevice_dropdown.open)
        self.electrodevice_dropdown.bind(on_select=lambda instance, x: setattr(self.electrodevice_button, 'text', x))

        electrodevice_items = [f'{electrodevices.iron.name}', f'{electrodevices.tv.name}', f'{electrodevices.vashingMachine.name}']

        for item in electrodevice_items:
            btn = Button(text=item, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.electrodevice_select(btn.text))
            self.electrodevice_dropdown.add_widget(btn)
    
        layout.add_widget(electrodevice_label) 
        layout.add_widget(self.electrodevice_button) 

        hours_label = Label(text="Введите количество часов использования")
        self.hours_input = TextInput()

        calculate_label = Label(text="")
        calculate_button = Button(text="Рассчитать")
        calculate_button.bind(on_press=self.calculate)

        layout.add_widget(hours_label)
        layout.add_widget(self.hours_input)
        layout.add_widget(calculate_label)
        layout.add_widget(calculate_button)

        self.result_label = Label(text="Результаты:")
        self.electricity_label = Label(text="Потребление электроэнергии:")
        space = Label(text="")
        self.coast_label = Label(text="Стоимость использования прибора:")

        layout.add_widget(self.result_label)
        layout.add_widget(self.electricity_label)
        layout.add_widget(space)
        layout.add_widget(self.coast_label)

        return layout

    def electrodevice_select(self, electrodevice):
        if electrodevice == f'{electrodevices.iron.name}':
            self.electrodevice_button.text = f'{electrodevices.iron.name}'

        elif electrodevice == f'{electrodevices.tv.name}':
            self.electrodevice_button.text = f'{electrodevices.tv.name}'

        else:
            self.electrodevice_button.text = f'{electrodevices.vashingMachine.name}'

        self.electrodevice_dropdown.dismiss() 

    def calculate(self, instance):
        tariff = 4
        hours = float(self.hours_input.text)

        if self.electrodevice_button.text == f'{electrodevices.iron.name}':
            electricity = hours * electrodevices.iron.power
            coast = electricity * tariff
        elif self.electrodevice_button.text == f'{electrodevices.tv.name}':
            electricity = hours * electrodevices.tv.power
            coast = electricity * tariff
        elif self.electrodevice_button.text == f'{electrodevices.vashingMachine.name}':
            electricity = hours * electrodevices.vashingMachine.power
            coast = electricity * tariff

        self.electricity_label.text = f"Потребление электроэнергии: {electricity:.2f} кВт"
        self.coast_label.text = f"Стоимость использования: {coast:.2f} руб"
        print(str(app))
        print(repr(app))
        docx_save.docx_save(self.electrodevice_button.text, hours, electricity, coast)
        return hours, electricity, coast
    
if __name__=="__main__":
    app = myApp()
    app.run()