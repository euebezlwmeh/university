#Расход электроэнергии (кВт.ч) = мощность (кВт) × время использования (ч) (A)
#Стоимость использования прибора за период = расход электроэнергии х тариф (C) 

from package import gui
import toga
from toga.style.pack import COLUMN

def build(app):
    box = toga.Box()

    container = toga.OptionContainer(
        content = [("Утюг", gui.iron_func()), ("ТВ", gui.tv_func()), ("Стиральная машина", gui.vashingmachine_func())]
    )

    box.add(container)
    box.style.update(direction=COLUMN, padding=10)

    return box

def main():
    return toga.App("6_laba", "6_laba", startup=build)

if __name__ == "__main__":
    main().main_loop()
