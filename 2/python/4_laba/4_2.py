#Декоратор для подавления вывода функции на консоль.

def decorator(func):
    def wrapper(*args, **kwargs):
        return
    return wrapper

@decorator
def simple_func():
    x = 2 + 3
    return x

print(simple_func())
