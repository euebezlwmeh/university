def func(x, k, b0 = None, y0 = 1):
    if x <= 0:
        print("Incorrect value!")
        return

    if b0 is None:
        b0 = 1 / (2 * x)

    if k == 0:
        return y0
    return func(x, k - 1, b0 * (x ** 2), b0 * y0)


print(func(1, 3))
