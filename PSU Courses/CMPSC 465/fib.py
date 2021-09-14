def fib1(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return fib1(x-1)+fib1(x-2)

def fib2(x):
    if x == 0:
        return 0
    a, b = 0, 1
    for i in range(x-1):
        a, b = b, a + b
    return b

print(fib2(25))