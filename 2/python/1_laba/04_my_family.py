my_family = ["Мама","Папа","Брат","Бабушка"]

my_family_height = [
    [my_family[0],160], #мама
    [my_family[1],167], #папа
    [my_family[2],177], #брат
    [my_family[3],152], #бабушка
]

print(f"Рост мамы - {my_family_height[0][1]} см")
print(f"Рост папы - {my_family_height[1][1]} см")
print(f"Рост брата - {my_family_height[2][1]} см")
print(f"Рост бабушки - {my_family_height[3][1]} см")

for x in range(len(my_family_height)):
    summa = sum([my_family_height[x][1]])

print(f"Общий рост моей семьи - {summa} см")
