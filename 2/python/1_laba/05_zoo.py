zoo = ['lion', 'kangaroo', 'elephant', 'monkey', ]
zoo.insert(1,"bear")
print(zoo)

birds = ['rooster', 'ostrich', 'lark', ]
zoo+=birds
print(zoo)

zoo.remove("elephant")
print(zoo)

print(zoo.index("lion")+1, zoo.index("lark")+1)
