"""
Simple Calculator (symbols + easy inputs)

Usage: run `python calculator.py` and follow the menu prompts.
You can choose an operation by number, name, or symbol (e.g. 1, +, add, ➕).
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
    # operations: key -> (display name, symbol, function)
    ops = {
        "1": ("Addition", "➕", add),
        "2": ("Subtraction", "➖", subtract),
        "3": ("Multiplication", "✖️", multiply),
        "4": ("Division", "➗", divide),
        "5": ("Power", "^", power),
        "6": ("Modulus", "%", modulus),
    }

    # map many possible user inputs to the operation key
    input_map = {}
    alternatives = {
        "1": ["+", "add", "plus", "➕"],
        "2": ["-", "sub", "subtract", "minus", "➖"],
        "3": ["*", "x", "×", "mul", "multiply", "✖️"],
        "4": ["/", "\\", "div", "divide", "÷", "➗"],
        "5": ["^", "**", "pow", "power"],
        "6": ["%", "mod", "modulo"],
    }

    for k in ops:
        # accept the number, the name, and symbol
        name = ops[k][0]
        sym = ops[k][1]
        input_map[k] = k
        input_map[name.lower()] = k
        input_map[sym.lower()] = k
        for alt in alternatives.get(k, []):
            input_map[alt.lower()] = k

    print("Simple Calculator — choose by number, name, or symbol")
    while True:
        print("\nSelect operation:")
        for k, (name, sym, _) in ops.items():
            print(f" {k}. {sym}  {name}")
        print(" 0. Exit")

        choice_raw = input("Enter choice (e.g. 1 or + or add): ").strip()
        choice = choice_raw.lower()
        if choice == "0" or choice == "exit":
            print("Goodbye!")
            break

        op_key = input_map.get(choice)
        if op_key is None:
            print("Invalid choice, please try again. You can enter a number (1-6), a symbol like + or ×, or words like 'add'.")
            continue

        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")
        _, sym, func = ops[op_key]
        try:
            result = func(a, b)
        except ZeroDivisionError as e:
            print(e)
            continue

        # Print whole numbers without trailing .0
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        print(f"Result ({sym}): {result}")


if __name__ == "__main__":
    main()
