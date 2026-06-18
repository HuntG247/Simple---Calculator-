"""
Enhanced Simple Calculator with Real Calculator UI

Features:
- Looks and feels like a real calculator
- Interactive grid-based button layout
- Persistent display screen showing current input and results
- Support for chaining operations (press = to see result, continue calculating)
- Command-line mode: `python calculator.py 2 + 3`
- REPL mode: `python calculator.py --repl`

Usage examples:
- Interactive calculator: `python calculator.py`
- One-off expression: `python calculator.py 2 + 3`
- REPL mode: `python calculator.py --repl`

"""

from typing import Callable, Optional
import argparse
import sys
import os


# ============================================================================
# Core Calculator Operations
# ============================================================================

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


# Operator mapping
OPERATORS = {
    "+": (add, "Add"),
    "-": (subtract, "Subtract"),
    "*": (multiply, "Multiply"),
    "/": (divide, "Divide"),
    "^": (power, "Power"),
    "%": (modulus, "Modulo"),
}

# Extended input mappings for all operator names
OPERATOR_NAMES = {
    "+": "+", "add": "+", "plus": "+",
    "-": "-", "sub": "-", "subtract": "-", "minus": "-",
    "*": "*", "x": "*", "mul": "*", "multiply": "*",
    "/": "/", "div": "/", "divide": "/",
    "^": "^", "**": "^", "pow": "^", "power": "^",
    "%": "%", "mod": "%", "modulo": "%",
}

TOKEN_TO_FUNC = {
    "+": add, "add": add, "plus": add,
    "-": subtract, "sub": subtract, "subtract": subtract, "minus": subtract,
    "*": multiply, "x": multiply, "mul": multiply, "multiply": multiply,
    "/": divide, "div": divide, "divide": divide,
    "^": power, "**": power, "pow": power, "power": power,
    "%": modulus, "mod": modulus, "modulo": modulus,
}


# ============================================================================
# Utility Functions
# ============================================================================

def format_result(res: float) -> str:
    """Format result, showing integers without decimal point."""
    if isinstance(res, float) and res.is_integer():
        return str(int(res))
    return str(res)


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def compute_tokens(a_tok: str, op_tok: str, b_tok: str, last_result: Optional[float] = None) -> float:
    """Compute result from token strings."""
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
    func = TOKEN_TO_FUNC.get(op_tok.lower())
    if func is None:
        raise ValueError(f"Unknown operator: {op_tok}")
    return func(a, b)


def one_off_expression(args: list[str], last_result: Optional[float] = None) -> Optional[float]:
    """Parse and compute a single expression from CLI arguments."""
    if not args:
        return None
    
    if len(args) == 1:
        raw = args[0].strip()
        for op in ["**", "+", "-", "*", "/", "%", "^"]:
            if op in raw and op != "-":
                parts = raw.split(op)
                if len(parts) == 2:
                    a_tok, b_tok = parts[0].strip(), parts[1].strip()
                    return compute_tokens(a_tok, op, b_tok, last_result)
    
    if len(args) >= 3:
        a_tok = args[0]
        op_tok = args[1]
        b_tok = args[2]
        return compute_tokens(a_tok, op_tok, b_tok, last_result)
    
    return None


# ============================================================================
# Calculator Display UI
# ============================================================================

class CalculatorUI:
    """A real-looking calculator interface."""
    
    def __init__(self):
        self.display = "0"
        self.current_input = ""
        self.operator = None
        self.first_operand = None
        self.new_number = True
    
    def draw_display(self):
        """Draw the calculator display screen."""
        print("\n" + "╔" + "═" * 40 + "╗")
        print("║" + " " * 40 + "║")
        
        # Show the display value (right-aligned)
        display_str = str(self.display)
        if len(display_str) > 35:
            display_str = display_str[-35:]
        padding = 35 - len(display_str)
        print(f"║{' ' * padding}{display_str}{' ' * 5}║")
        print("║" + " " * 40 + "║")
        print("╚" + "═" * 40 + "╝\n")
    
    def draw_buttons(self):
        """Draw the calculator button grid."""
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["C", "^", "%", "←"],
        ]
        
        button_width = 9
        
        for row in buttons:
            print("  ", end="")
            for btn in row:
                print(f"┌─────────┐", end="  ")
            print()
            
            print("  ", end="")
            for btn in row:
                centered = btn.center(9)
                print(f"│{centered}│", end="  ")
            print()
            
            print("  ", end="")
            for btn in row:
                print(f"└─────────┘", end="  ")
            print()
    
    def process_input(self, btn: str) -> bool:
        """Process a button press. Returns False if calculator should exit."""
        
        if btn == "C":
            # Clear
            self.display = "0"
            self.current_input = ""
            self.operator = None
            self.first_operand = None
            self.new_number = True
        
        elif btn == "←":
            # Backspace
            if self.current_input:
                self.current_input = self.current_input[:-1]
                self.display = self.current_input if self.current_input else "0"
            elif self.display != "0":
                self.display = self.display[:-1] if len(self.display) > 1 else "0"
        
        elif btn == ".":
            # Decimal point
            if self.new_number:
                self.current_input = "0."
                self.display = "0."
                self.new_number = False
            elif "." not in self.current_input:
                self.current_input += "."
                self.display = self.current_input
        
        elif btn.isdigit():
            # Number input
            if self.new_number:
                self.current_input = btn
                self.new_number = False
            else:
                self.current_input += btn
            self.display = self.current_input
        
        elif btn in OPERATORS or btn == "^" or btn == "%":
            # Operator
            if self.operator and self.current_input and self.first_operand is not None:
                # Chain calculation
                try:
                    result = compute_tokens(str(self.first_operand), self.operator, self.current_input)
                    self.first_operand = result
                    self.display = format_result(result)
                except ZeroDivisionError:
                    self.display = "Error: Division by zero"
                except Exception as e:
                    self.display = f"Error: {str(e)}"
                self.current_input = ""
            elif self.current_input:
                try:
                    self.first_operand = float(self.current_input)
                except ValueError:
                    self.display = "Error: Invalid number"
                    return True
                self.current_input = ""
            elif self.first_operand is None:
                try:
                    self.first_operand = float(self.display)
                except ValueError:
                    self.display = "Error: Invalid number"
                    return True
            
            self.operator = btn
            self.new_number = True
        
        elif btn == "=":
            # Calculate
            if self.operator and self.current_input and self.first_operand is not None:
                try:
                    result = compute_tokens(str(self.first_operand), self.operator, self.current_input)
                    self.display = format_result(result)
                    self.first_operand = result
                    self.current_input = ""
                    self.operator = None
                    self.new_number = True
                except ZeroDivisionError:
                    self.display = "Error: Division by zero"
                except Exception as e:
                    self.display = f"Error: {str(e)}"
            elif self.first_operand is not None:
                self.display = format_result(self.first_operand)
                self.current_input = ""
        
        return True
    
    def run(self) -> int:
        """Run the interactive calculator."""
        try:
            while True:
                clear_screen()
                print("\n" + "=" * 50)
                print("         CALCULATOR".center(50))
                print("=" * 50)
                
                self.draw_display()
                self.draw_buttons()
                
                print("\n  (Enter button or type 'quit' to exit)")
                user_input = input("  Button: ").strip().lower()
                
                if user_input == "quit":
                    clear_screen()
                    print("Thank you for using Calculator!")
                    return 0
                
                # Match input to button
                valid_buttons = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-",
                                "0", ".", "=", "+", "c", "^", "%", "←", "backspace"]
                
                if user_input in valid_buttons:
                    btn = user_input
                    if btn == "backspace":
                        btn = "←"
                    if btn == "c":
                        btn = "C"
                    self.process_input(btn)
                else:
                    print("Invalid button. Please try again.")
                    input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\nCalculator closed.")
            return 0


# ============================================================================
# REPL Mode
# ============================================================================

def repl_mode() -> int:
    """Run REPL mode for chaining calculations."""
    print("\n" + "=" * 50)
    print("         CALCULATOR - REPL MODE".center(50))
    print("=" * 50)
    print("\nEnter expressions like: 2 + 3")
    print("Use '_' to reference the last result")
    print("Type 'quit' or 'exit' to exit.\n")
    
    last = None
    
    try:
        while True:
            raw = input("> ").strip()
            
            if not raw:
                continue
            
            if raw.lower() in ("quit", "exit"):
                print("Goodbye!")
                return 0
            
            tokens = raw.split()
            
            try:
                res = one_off_expression(tokens, last)
                if res is None:
                    print("Could not parse expression. Try: number operator number")
                    continue
                last = res
                print(f"= {format_result(res)}\n")
            except ZeroDivisionError as e:
                print(f"Error: {e}\n")
            except Exception as e:
                print(f"Error: {e}\n")
    
    except KeyboardInterrupt:
        print("\n\nCalculator closed.")
        return 0


# ============================================================================
# Main
# ============================================================================

def main(argv: Optional[list[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Simple Calculator — Interactive UI, CLI, and REPL modes",
        prog="calculator"
    )
    parser.add_argument("expr", nargs="*", help="One-off expression (e.g., '2 + 3')")
    parser.add_argument("--repl", action="store_true", help="Start REPL mode for chaining calculations")
    
    ns = parser.parse_args(argv)

    # REPL mode
    if ns.repl:
        return repl_mode()

    # One-off expression
    if ns.expr:
        try:
            res = one_off_expression(ns.expr)
            if res is None:
                print("Could not parse expression. Use: number operator number")
                return 2
            print(format_result(res))
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 3

    # Interactive calculator UI
    calc = CalculatorUI()
    return calc.run()


if __name__ == "__main__":
    raise SystemExit(main())
