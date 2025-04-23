goods = {
    'Лампа': '12345',
    'Стол': '23456',
    'Диван': '34567',
    'Стул': '45678',
}

store = {
    '12345': [
        {'quantity': 27, 'price': 42},
    ],
    '23456': [
        {'quantity': 22, 'price': 510},
        {'quantity': 32, 'price': 520},
    ],
    '34567': [
        {'quantity': 2, 'price': 1200},
        {'quantity': 1, 'price': 1150},
    ],
    '45678': [
        {'quantity': 50, 'price': 100},
        {'quantity': 12, 'price': 95},
        {'quantity': 43, 'price': 97},
    ],
}

#lamps
lamp_code = goods['Лампа']
lamps_item = store[lamp_code][0]
lamps_quantity = lamps_item['quantity']
lamps_price = lamps_item['price']
lamps_cost = lamps_quantity * lamps_price

#tables
table_code = goods['Стол']
tables_item1 = store[table_code][0]
tables_item2 = store[table_code][1]

tables_quantity1 = tables_item1['quantity']
tables_quantity2 = tables_item2['quantity']
tables_quantity = tables_quantity1 + tables_quantity2

tables_price1 = tables_item1['price']
tables_price2 = tables_item2['price']
tables_cost = (tables_quantity1 * tables_price1) + (tables_quantity2 * tables_price2)

#sofa
sofa_code = goods['Диван']
sofa_item1 = store[sofa_code][0]
sofa_item2 = store[sofa_code][1]

sofa_quantity1 = sofa_item1['quantity']
sofa_quantity2 = sofa_item2['quantity']
sofa_quantity = sofa_quantity1 + sofa_quantity2

sofa_price1 = sofa_item1['price']
sofa_price2 = sofa_item2['price']
sofa_cost = (sofa_quantity1 * sofa_price1) + (sofa_quantity2 * sofa_price2)

#chair
chair_code = goods['Стул']
chair_item1 = store[chair_code][0]
chair_item2 = store[chair_code][1]
chair_item3 = store[chair_code][2]

chair_quantity1 = chair_item1['quantity']
chair_quantity2 = chair_item2['quantity']
chair_quantity3 = chair_item3['quantity']
chair_quantity = chair_quantity1 + chair_quantity2 + chair_quantity3

chair_price1 = chair_item1['price']
chair_price2 = chair_item2['price']
chair_price3 = chair_item3['price']
chair_cost = (chair_quantity1 * chair_price1) + (chair_quantity2 * chair_price2) + (chair_quantity3 * chair_price3)

print('Лампа -', lamps_quantity, 'шт, стоимость', lamps_cost, 'руб')
print('Стол -', tables_quantity, 'шт, стоимость', tables_cost, 'руб')
print('Диван -', sofa_quantity, 'шт, стоимость', sofa_cost, 'руб')
print('Стул -', chair_quantity, 'шт, стоимость', chair_cost, 'руб')
