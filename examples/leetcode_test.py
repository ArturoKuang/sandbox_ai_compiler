a: int = 15
b: int = 42
c: int = 27
max: int = a
if (b > max):
    max = b
if (c > max):
    max = c
print(max)
counter: int = 10
while (counter > 0):
    print(counter)
    counter = (counter - 1)
isPositive: bool = (counter >= 0)
print(isPositive)
isNegative: bool = (counter < 0)
print(isNegative)
n: int = 10
fib1: int = 0
fib2: int = 1
count: int = 0
print(fib1)
print(fib2)
while (count < (n - 2)):
    next: int = (fib1 + fib2)
    print(next)
    fib1 = fib2
    fib2 = next
    count = (count + 1)
x: int = 5
y: int = 10
result1: bool = ((x < y) and (y > 0))
print(result1)
result2: bool = ((x == y) or (x < y))
print(result2)
result3: bool = (not (x > y))
print(result3)