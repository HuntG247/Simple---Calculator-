"""
Enhanced Simple Calculator (fully Python)

Features added:
- Keeps the previous interactive menu with boxed symbols and flexible input (number, name, symbol).
- Adds a command-line expression mode: `python calculator.py 2 + 3` or `python calculator.py "2 + 3"` to compute a single expression.
- Adds a REPL mode: `python calculator.py --repl` to chain calculations using `_` to refer to the last result.
- Adds a small, safe expression parser for `number operator number` (no eval), accepting symbols and words.
- Improved formatting for integer results.
- Functions are exported for easy unit testing.

Usage examples:
- Interactive menu: `python calculator.py`
- One-off expression: `python calculator.py 2 + 3`
- One-off expression (quoted): `python calculator.py "2 + 3"`
- REPL mode: `python calculator.py --repl`

"""

from typing import Callable, Optional
import argparse
import sys
import operator

# Public operation functions

def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def power(a: float, b: float) -> float:
    return a ** b


def modulus(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot modulo by zero")
    return a % b

# Mapping of operation keys to (name, symbol, function)
ops = {
    "1": ("Addition", "➕", add),
    "2": ("Subtraction", "➖", subtract),
    "3": ("Multiplication", "✖", multiply),
    "4": ("Division", "➗", divide),
    "5": ("Power", "^", power),
    "6": ("Modulus", "%", modulus),
}

# Alternate inputs that map to an op key
alternatives = {
    "1": ["+", "add", "plus", "➕"],
    "2": ["-", "sub", "subtract", "minus", "➖"],
    "3": ["*", "x", "×", "mul", "multiply", "✖", "✖️"],
    "4": ["/", "\\", "div", "divide", "÷", "➗"],
    "5": ["^", "**", "pow", "power"],
    "6": ["%", "mod", "modulo"],
}

# Build a lookup from user input to operation key
input_map = {}
for k in ops:
    name = ops[k][0]
    sym = ops[k][1]
    input_map[k] = k
    input_map[name.lower()] = k
    input_map[sym.lower()] = k
    for alt in alternatives.get(k, []):
        input_map[alt.lower()] = k

# For one-off CLI parsing: map common operator tokens to functions
token_to_func: dict[str, Callable[[float, float], float]] = {
    "+": add,
    "add": add,
    "plus": add,
    "-": subtract,
    "sub": subtract,
    "subtract": subtract,
    "minus": subtract,
    "*": multiply,
    "x": multiply,
    "×": multiply,
    "mul": multiply,
    "multiply": multiply,
    "✖": multiply,
    "✖️": multiply,
    "/": divide,
    "\\": divide,
    "div": divide,
    "divide": divide,
    "÷": divide,
    "^": power,
    "**": power,
    "pow": power,
    "power": power,
    "%": modulus,
    "mod": modulus,
    "modulo": modulus,
}


def print_boxed_symbol(sym: str) -> None:
    # Center a short symbol inside a 7-char wide box for better presentation
    width = 7
    pad = (width - len(sym)) // 2
    s = " " * pad + sym + " " * (width - len(sym) - pad)
    print("╔" + "═" * width + "╗")
    print(f"║{s}║")
    print("╚" + "═" * width + "╝")


def get_number(prompt: str, last_result: Optional[float] = None) -> float:
    while True:
        raw = input(prompt).strip()
        if raw == "_" and last_result is not None:
            return last_result
        try:
            # Accept integers and floats
            if "." in raw:
                return float(raw)
            return int(raw) if raw.lstrip("-+").isdigit() else float(raw)
        except ValueError:
            print("Please enter a valid number (or '_' to use the last result).")


def format_result(res: float) -> str:
    if isinstance(res, float) and res.is_integer():
        return str(int(res))
    return str(res)


def compute_tokens(a_tok: str, op_tok: str, b_tok: str, last_result: Optional[float] = None) -> float:
    # Convert tokens into numbers, support '_' for last_result
    def to_number(tok: str) -> float:
        if tok == "_":
            if last_result is None:
                raise ValueError("No previous result available for '_'.")
            return last_result
        try:
            return int(tok) if tok.lstrip("-+").isdigit() else float(tok)
        except ValueError:
            raise ValueError(f"Invalid number: {tok}")

    a = to_number(a_tok)
    b = to_number(b_tok)
    func = token_to_func.get(op_tok.lower())
    if func is None:
        raise ValueError(f"Unknown operator: {op_tok}")
    return func(a, b)


def one_off_expression(args: list[str], last_result: Optional[float] = None) -> Optional[float]:
    # Accept either: ["2", "+", "3"] or ["2+3"] or ["2", "+3"] etc.
    if not args:
        return None
    # If single argument, try to split by spaces or common ops
    if len(args) == 1:
        raw = args[0].strip()
        # try space-separated tokens inside
        for sep in [" ", "+", "-", "*", "/", "%", "^", "**"]:
            if sep in raw and not raw.startswith("_"):
                # special-case - for negative numbers, split carefully
                # We'll try a simple approach: attempt to parse as 'a op b' with operators as token separators
                for op in ["**", "+", "-", "*", "/", "%", "^"]:
                    if op in raw and op != "-":
                        parts = raw.split(op)
                        if len(parts) == 2:
                            a_tok, b_tok = parts[0].strip(), parts[1].strip()
                            return compute_tokens(a_tok, op, b_tok, last_result)
                # handle minus: try to find the operator in the middle
                # e.g. -2--3 or 2--3 are ambiguous; skip complex cases here
        # fallback: try eval-like parsing via whitespace
    if len(args) >= 3:
        a_tok = args[0]
        op_tok = args[1]
        b_tok = args[2]
        return compute_tokens(a_tok, op_tok, b_tok, last_result)
    return None


def interactive_menu(last_result: Optional[float] = None) -> Optional[float]:
    print("Simple Calculator — visual symbols menu (choose by number, name, or symbol)")
    while True:
        print("\nSelect operation (or type 'exit' to quit):\n")
        for k, (name, sym, _) in ops.items():
            print_boxed_symbol(sym)
            print(f" {k}. {name}\n")

        choice_raw = input("Enter choice (e.g. 1 or + or add): ").strip()
        choice = choice_raw.lower()
        if choice == "0" or choice == "exit":
            print("Goodbye!")
            return None

        op_key = input_map.get(choice)
        if op_key is None:
            print("Invalid choice, please try again. You can enter a number (1-6), a symbol like + or ×, or words like 'add'.")
            continue

        a = get_number("Enter first number: ", last_result)
        b = get_number("Enter second number: ", last_result)
        _, sym, func = ops[op_key]
        try:
            result = func(a, b)
        except ZeroDivisionError as e:
            print(e)
            continue

        print(f"Result ({sym}): {format_result(result)}")
        return result


def repl_mode() -> None:
    print("REPL mode — enter expressions like: 2 + 3   (use _ for last result). Type 'quit' to exit.")
    last = None
    while True:
        raw = input("> ").strip()
        if not raw:
            continue
        if raw.lower() in ("quit", "exit"):
            break
        # try to split into tokens naively
        tokens = raw.split()
        try:
            res = one_off_expression(tokens, last)
            if res is None:
                print("Could not parse expression. Try: number operator number")
                continue
            last = res
            print(format_result(res))
        except Exception as e:
            print("Error:", e)


def main(argv: Optional[list[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Simple Calculator — CLI and interactive modes")
    parser.add_argument("expr", nargs="*", help="One-off expression, e.g. 2 + 3 or '2 + 3'", )
    parser.add_argument("--repl", action="store_true", help="Start REPL mode to chain calculations")
    ns = parser.parse_args(argv)

    # REPL mode
    if ns.repl:
        repl_mode()
        return 0

    # One-off expression from CLI arguments
    if ns.expr:
        try:
            res = one_off_expression(ns.expr)
            if res is None:
                print("Could not parse expression. Use: number operator number")
                return 2
            print(format_result(res))
            return 0
        except Exception as e:
            print("Error:", e)
            return 3

    # Otherwise, fall back to interactive menu
    last = None
    while True:
        res = interactive_menu(last)
        if res is None:
            break
        last = res
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
