
def checkPalindrom(n):
    reversed_num = 0
    num = n
    while num != 0:
        digit = num % 10
        reversed_num = reversed_num * 10 + digit
        num //= 10
    return reversed_num == n

print(checkPalindrom(12021))
print(checkPalindrom(1231))