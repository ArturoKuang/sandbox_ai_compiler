int a = 15;
int b = 42;
int c = 27;

int max = a;

if (b > max) {
    max = b;
}

if (c > max) {
    max = c;
}

print(max);

int counter = 10;
while (counter > 0) {
    print(counter);
    counter = counter - 1;
}

bool isPositive = counter >= 0;
print(isPositive);

bool isNegative = counter < 0;
print(isNegative);

int n = 10;
int fib1 = 0;
int fib2 = 1;
int count = 0;

print(fib1);
print(fib2);

while (count < n - 2) {
    int next = fib1 + fib2;
    print(next);
    fib1 = fib2;
    fib2 = next;
    count = count + 1;
}

int x = 5;
int y = 10;

bool result1 = x < y && y > 0;
print(result1);

bool result2 = x == y || x < y;
print(result2);

bool result3 = !(x > y);
print(result3);
