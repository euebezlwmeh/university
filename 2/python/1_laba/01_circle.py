radius = 42
pi = 3.1415926
S = pi * radius**2 

print(round(S, 4))

point_1 = (23, 34) 
x1 = 23
y1 = 34

point_2 = (30, 30)
x2 = 30
y2 = 30

def func(x, y):
    return (x**2 + y**2)**0.5 < radius

print(func(x1, y1))
print(func(x2, y2))
