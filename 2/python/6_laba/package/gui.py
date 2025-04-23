from package import values, docx_save
import toga
from toga.style.pack import COLUMN, LEFT, RIGHT, ROW, Pack

def iron_func():

    name = "Утюг"
    box1 = toga.Box()
    iron_calculate_box = toga.Box()
    iron_calculate_box = toga.Box()
    iron_box = toga.Box()
    
    iron_calculate_A = toga.Box()
    iron_calculate_C = toga.Box()

    iron_days = toga.TextInput()
    iron_calculate_A = toga.TextInput(readonly=True)
    iron_calculate_C = toga.TextInput(readonly=True)

    iron_label = toga.Label("Кол-во часов исп. утюга", style=Pack(text_align=RIGHT))
    iron_label_A = toga.Label("Расход энергии для утюга", style=Pack(text_align=LEFT))
    iron_label_C = toga.Label("Стоим. исп. для утюга", style=Pack(text_align=LEFT))
    
    def iron(widget):
        try:
            iron_calculate_A.value = values.pIron * (float(iron_days.value))
            iron_calculate_C.value = float(iron_calculate_A.value) * values.tarif
            docx_save.docx_save(name, iron_days.value, str(iron_calculate_A.value), str(iron_calculate_C.value))
        except ValueError:
            iron_calculate_A.value = "Введите кол-во часов"
            iron_calculate_C.value = "Введите кол-во часов"

    ironButton = toga.Button("Calculate and save in docx", on_press=iron)

    iron_box.add(iron_label)
    iron_box.add(iron_days)
    iron_box.add(ironButton)
    iron_calculate_box.add(iron_label_A)
    iron_calculate_box.add(iron_calculate_A)
    iron_calculate_box.add(iron_label_C)
    iron_calculate_box.add(iron_calculate_C)

    box1.add(iron_box)
    box1.add(iron_calculate_box)
    
    box1.style.update(direction=COLUMN, padding=10)
    iron_box.style.update(direction=ROW, padding=5)
    iron_calculate_box.style.update(direction=ROW, padding=5)

    return box1

def tv_func():

    name = "ТВ"
    box2 = toga.Box()
    tv_calculate_box = toga.Box()
    tv_calculate_box = toga.Box()
    tv_box = toga.Box()
    
    tv_calculate_A = toga.Box()
    tv_calculate_C = toga.Box()

    tv_days = toga.TextInput()
    tv_calculate_A = toga.TextInput(readonly=True)
    tv_calculate_C = toga.TextInput(readonly=True)

    tv_label = toga.Label("Кол-во часов исп. ТВ", style=Pack(text_align=RIGHT))
    tv_label_A = toga.Label("Расход энергии для ТВ", style=Pack(text_align=LEFT))
    tv_label_C = toga.Label("Стоим. исп. для ТВ", style=Pack(text_align=LEFT))
    
    def tv(widget):
        try:
            tv_calculate_A.value = values.pTv * (float(tv_days.value))
            tv_calculate_C.value = float(tv_calculate_A.value) * values.tarif
            docx_save.docx_save(name, tv_days.value, str(tv_calculate_A.value), str(tv_calculate_C.value))
        except ValueError:
            tv_calculate_A.value = "Введите кол-во часов"
            tv_calculate_C.value = "Введите кол-во часов"
           
    tvButton = toga.Button("Calculate and save in docx", on_press=tv)

    tv_box.add(tv_label)
    tv_box.add(tv_days)
    tv_box.add(tvButton)
    tv_calculate_box.add(tv_label_A)
    tv_calculate_box.add(tv_calculate_A)
    tv_calculate_box.add(tv_label_C)
    tv_calculate_box.add(tv_calculate_C)

    box2.add(tv_box)
    box2.add(tv_calculate_box)
    
    box2.style.update(direction=COLUMN, padding=10)
    tv_box.style.update(direction=ROW, padding=5)
    tv_calculate_box.style.update(direction=ROW, padding=5)

    return box2

def vashingmachine_func():

    name = "Стиральная машина"
    box3 = toga.Box()
    vashingmachine_calculate_box = toga.Box()
    vashingmachine_calculate_box = toga.Box()
    vashingmachine_box = toga.Box()
    
    vashingmachine_calculate_A = toga.Box()
    vashingmachine_calculate_C = toga.Box()

    vashingmachine_days = toga.TextInput()
    vashingmachine_calculate_A = toga.TextInput(readonly=True)
    vashingmachine_calculate_C = toga.TextInput(readonly=True)

    vashingmachine_label = toga.Label("Кол-во часов исп. стиральной машины", style=Pack(text_align=RIGHT))
    vashingmachine_label_A = toga.Label("Расход энергии для стиральной машины", style=Pack(text_align=LEFT))
    vashingmachine_label_C = toga.Label("Стоим. использ. для стиральной машины", style=Pack(text_align=LEFT))
    
    def vashingmachine(widget):
        try:
            vashingmachine_calculate_A.value = values.pVashingMachine * (float(vashingmachine_days.value))
            vashingmachine_calculate_C.value = float(vashingmachine_calculate_A.value) * values.tarif
            docx_save.docx_save(name, vashingmachine_days.value, str(vashingmachine_calculate_A.value), str(vashingmachine_calculate_C.value))
        except ValueError:
            vashingmachine_calculate_A.value = "Введите кол-во часов"
            vashingmachine_calculate_C.value = "Введите кол-во часов"

    vashingmachineButton = toga.Button("Calculate and save in docx", on_press=vashingmachine)

    vashingmachine_box.add(vashingmachine_label)
    vashingmachine_box.add(vashingmachine_days)
    vashingmachine_box.add(vashingmachineButton)
    vashingmachine_calculate_box.add(vashingmachine_label_A)
    vashingmachine_calculate_box.add(vashingmachine_calculate_A)
    vashingmachine_calculate_box.add(vashingmachine_label_C)
    vashingmachine_calculate_box.add(vashingmachine_calculate_C)

    box3.add(vashingmachine_box)
    box3.add(vashingmachine_calculate_box)
    
    box3.style.update(direction=COLUMN, padding=10)
    vashingmachine_box.style.update(direction=ROW, padding=5)
    vashingmachine_calculate_box.style.update(direction=ROW, padding=5)

    return box3