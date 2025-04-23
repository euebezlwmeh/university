def create_n_dim_array(n, x):
    for i in range(n - 2):         
        print('\t' * i, '[')

    for i in range(n - 1):
        print('\t' * (n - 2), '[')
        for j in range(x):
            print('\t' * (n-1), [f'level {n}'] * x)
        print('\t' * (n - 2), ']')

    for i in range(n - 3, -1, -1): 
        print('\t' * i, ']')

n = int(input("Enter n: "))
x = int(input("Enter x: "))
create_n_dim_array(n, x)
