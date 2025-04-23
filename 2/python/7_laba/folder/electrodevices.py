class Electrodevice:
    def __init__(self, name: str, power: float):
        self.name = name
        self.power = power

    @property
    def func(self):
        return self.name
    
    @func.setter
    def func(self):
        return 

    def __repr__(self):
        return f'electrodevice({self.name, self.power})'

iron = Electrodevice("Утюг", 1)
tv = Electrodevice("ТВ", 0.084645)
vashingMachine = Electrodevice("Стиральная машина", 1.5)

print(iron, tv, vashingMachine)
