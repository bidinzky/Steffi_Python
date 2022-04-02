
def checkPalindrom(n):
    reversed_num = 0
    num = n #copy n into num, because we modify num but we need n for the comparision later
    while num != 0:
        digit = num % 10 #get the lowest digit of the number e.g. 1234 % 10 = 4 
        reversed_num = reversed_num * 10 + digit #shift all existing digits to the right (*10) and the newest one
        num //= 10 # integer divide by 10 to 1234 // 10 = 123 --> ignores decimal points
    return reversed_num == n #check if reversed number equals original

print(checkPalindrom(12021))
print(checkPalindrom(1231))