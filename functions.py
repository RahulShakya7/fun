def add():
    a = int(input('a:'))
    b = int(input('b:'))
    print(f'The sum of {a} and {b} is {a + b}')


add()


def sub():
    a = int(input('a:'))
    b = int(input('b:'))
    print(f'The subtraction of {a} and {b} is {a - b}')
    return {a - b}


sub()


def mul(a, b):
    ans = a * b
    print(f'The multiplication of {a} and {b} is {ans}')


x = int(input('a:'))
y = int(input('b:'))
mul(x,y)


def div(a, b):
    a = int(input('a:'))
    b = int(input('b:'))
    print(f'The sum of {a} and {b} is {a / b}')
    return (a / b)


x = int(input('a:'))
y = int(input('b:'))
div(x,y)
