sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}

distances = {}

for c1 in sites:
    for c2 in sites:
        if c1 != c2 and not distances.get((c2, c1)):
            x1, y1 = sites[c1]
            x2, y2 = sites[c2]
            s = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            distances[(c1, c2)] = s
            
for (a, b), d in distances.items():
    print(f"{a} - {b}: {d}")
