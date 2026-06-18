"""
Simple Calculator

Usage: run `python calculator.py` and follow the menu prompts.
Supports: addition, subtraction, multiplication, division, power, modulus.
Handles invalid input and division by zero.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def power(a, b):
    return a ** b


def modulus(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot modulo by zero")
    return a % b


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def main():
    ops = {
        "1": ("Addition", add),
        "2": ("Subtraction", subtract),
        "3": ("Multiplication", multiply),
        "4": ("Division", divide),
        "5": ("Power", power),
        "6": ("Modulus", modulus),
    }

    print("Simple Calculator")
    while True:
        print("\nSelect operation:")
        for k, (name, _) in ops.items():
            print(f" {k}. {name}")
        print(" 0. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "0":
            print("Goodbye!")
            break

        if choice not in ops:
            print("Invalid choice, please try again.")
            continue

        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")
        _, func = ops[choice]
        try:
            result = func(a, b)
        except ZeroDivisionError as e:
            print(e)
            continue

        # If result is an integer value, print without decimal places
        if result == int(result):
            result = int(result)
        print(f"Result: {result}")


if __name__ == "__main__":
    main()
