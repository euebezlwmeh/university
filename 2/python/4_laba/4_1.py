#Замыкание для отслеживания количества HP героя - HP не может 
#подниматься больше 100 и опускаться ниже 0, герой может лечиться 
#или получать урон.


def decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return min(max(result, 0), 100)
    return wrapper

def hero():
    hp = 100

    @decorator
    def heal(x):
        nonlocal hp 
        hp += x      #hp = min(hp + x, 100)
        return hp
    
    @decorator
    def damage(x):
        nonlocal hp
        hp -= x      #hp = max(hp - x, 0)
        return hp
    
    return heal, damage

heal, damage = hero()
print(damage(30))
print(heal(40))
