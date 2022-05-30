def Legopyramide(h):
    # number of stones is 1^2 + 2^2 + ... + h^2
    num = 0
    for i in range(1, h + 1):  # h+1 because range is exclusive
        num += i ** 2
    return num


assert (Legopyramide(4) == 30)
assert (Legopyramide(5) == 55)
