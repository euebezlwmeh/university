garden = ('ромашка', 'роза', 'одуванчик', 'ромашка', 'гладиолус', 'подсолнух', 'роза', )
meadow = ('клевер', 'одуванчик', 'ромашка', 'клевер', 'мак', 'одуванчик', 'ромашка', )

garden_set = set(garden)
meadow_set = set(meadow)

flowers = garden_set.union(meadow_set)
print("Все виды цветов:", flowers)

tut_i_tam = garden_set.intersection(meadow_set)
print("Цветы, растущие и в саду, и на лугу:", tut_i_tam)

unique_garden_flowers = garden_set.difference(meadow_set)
print("Цветы, растущие только в саду:", unique_garden_flowers)

unique_meadow_flowers = meadow_set.difference(garden_set)
print("Цветы, растущие только на лугу:", unique_meadow_flowers)
