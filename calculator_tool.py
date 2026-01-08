# This function adds two numbers
def add(x, y):
    return x + y


# This function subtracts two numbers
def subtract(x, y):
    return x - y


# This function multiplies two numbers
def multiply(x, y):
    return x * y


# This function divides two numbers
def divide(x, y):
    return x / y



def use_calculator(num1, num2, operation):

    # check if choice is one of the four options
    # Select operation.
    # 1.Add
    # 2.Subtract
    # 3.Multiply
    # 4.Divide

    if operation in (1, 2, 3, 4):

        if operation == 1:
            return f"\nCalculator Input: {num1} + {num2}\nCalculator output: {add(num1, num2)}"

        elif operation == 2:
            return f"\nCalculator Input: {num1} - {num2}\nCalculator output: {subtract(num1, num2)}"

        elif operation == 3:
            return f"\nCalculator Input: {num1} * {num2}\nCalculator output: {multiply(num1, num2)}"

        elif operation == 4:
            return f"\nCalculator Input: {num1} / {num2}\nCalculator output: {divide(num1, num2)}"


    return "\nCalculator output: Invalid Input"

# print(use_calculator(5, 4, 4))
