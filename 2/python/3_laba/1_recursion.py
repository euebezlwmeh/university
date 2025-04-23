def create_n_dim_array(n, x, level = 2):
    if n <= 1:
        print("\t"*(level-2), [f'level {level - 1}']*x)
        return None
    print("\t"*(level-2), "[")
    for i in range (x):
        (create_n_dim_array(n-1, x, level + 1))
    print("\t"*(level-2), "]")


n = int(input("Enter n: "))
x = int(input("Enter x: "))

create_n_dim_array(n, x)
