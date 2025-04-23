def func(x, k):
    if x <= 0:
        print("Incorrect value!")
        return
    b0 = 1 / (2 * x)
    y0 = 1

    while k != 0:
        bk = b0 * (x ** 2)
        yk = bk * y0

        b0 = bk
        y0 = yk

        k = k - 1
    return y0

print(func(1, 3))
