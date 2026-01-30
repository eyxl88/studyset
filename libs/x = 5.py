n = 5
if n > 0:
    print("one ")
if n < 0:
    print("two ")
else:
    print("three ")

x = 5
if x == 8: # SyntaxError x == 8: Nothing works before it, not even unrealted print.
    print("x is 8")
else:
    print("x is not 8")

def calculate():
    num1 = float(input("Enter a number here: "))
    num2 = float(input("Enter another number here: "))
    operation = input("Enter your operation here (add, "\
    "subtract, multiply, divide, or power): ")

    if operation == "add":
        print(num1, "+", num2)
        print(round(num1 + num2, 2))
    elif operation == "subtract":
        print(num1, "-", num2)
        print(round(num1 - num2, 2))
    elif operation == "multiply":
        print(num1, "*", num2)
        print(round(num1 * num2, 2))
    elif operation == "divide":
        print(num1, "/", num2)
        print(round(num1 / num2, 2))
    elif operation == "power":
        print(num1, "**", num2)
        print(round(pow(num1, num2)))

calculate()


# TODO: Reorganize the following code with the necessary spaces (indentation) 
#     and remove any unnecessary lines
# No character per line limitation in this part
# No comment is needed in this part

# Emily Lim
# 261278115
import math

print("Enter the coefficient a: ")
x = input()
a = float(x)

print("Enter the coefficient b: ")
y = input()
b = float(y)

print("Enter the coefficient c: ")
z = input()
c = float(z)

discriminant = b**2 - 4 * a * c

if discriminant > 0:
    root1 = (-b + math.sqrt(discriminant)) / (2 * a)
    root2 = (-b - math.sqrt(discriminant)) / (2 * a)
    print("The roots are:", root1, "and", root2)

elif discriminant == 0:
    root = -b/(2 * a)
    print("The equation has repeated real roots", root)

else:
    print("The equation has complex roots.")