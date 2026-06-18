"""
Enhanced Simple Calculator with Modern GUI

Features:
- Modern desktop GUI with dark theme
- Colorful, interactive buttons with hover effects
- Large, readable display screen
- Support for basic arithmetic operations
- Keyboard support for all operations
- History display showing previous calculations
- Real calculator feel with smooth interactions
- Error handling with user-friendly messages

Usage:
- Run: `python calculator.py`

"""

import tkinter as tk
from tkinter import font
import math
from typing import Optional


# ============================================================================
# Color Scheme
# ============================================================================

COLORS = {
    "bg_dark": "#1e1e1e",
    "bg_darker": "#121212",
    "display_bg": "#2d2d2d",
    "display_text": "#00ff88",
    "history_text": "#888888",
    "button_number": "#3d3d3d",
    "button_number_hover": "#4d4d4d",
    "button_operator": "#ff6b35",
    "button_operator_hover": "#ff8555",
    "button_equals": "#00d084",
    "button_equals_hover": "#00ff9d",
    "button_clear": "#e74c3c",
    "button_clear_hover": "#ff6b6b",
    "text_primary": "#ffffff",
    "text_secondary": "#888888",
}


# ============================================================================
# Core Calculator Operations
# ============================================================================

class Calculator:
    """Core calculator logic."""
    
    def __init__(self):
        self.expression = ""
        self.result = None
        self.history = []
    
    def add_character(self, char: str) -> str:
        """Add a character to the expression."""
        if char == "." and "." in self.expression.split()[-1:]:
            return self.expression
        self.expression += str(char)
        return self.expression
    
    def backspace(self) -> str:
        """Remove last character."""
        self.expression = self.expression[:-1]
        return self.expression
    
    def clear(self) -> str:
        """Clear the expression."""
        self.expression = ""
        self.result = None
        return self.expression
    
    def calculate(self) -> str:
        """Evaluate the expression."""
        if not self.expression:
            return ""
        
        try:
            # Replace ÷ and × with / and *
            expr = self.expression.replace("÷", "/").replace("×", "*").replace("^", "**")
            
            # Evaluate the expression
            result = eval(expr)
            
            # Store in history
            self.history.append(f"{self.expression} = {result}")
            if len(self.history) > 10:
                self.history.pop(0)
            
            self.expression = str(result)
            self.result = result
            return self.expression
        
        except ZeroDivisionError:
            self.expression = ""
            return "Error: Division by zero"
        except SyntaxError:
            self.expression = ""
            return "Error: Invalid expression"
        except Exception as e:
            self.expression = ""
            return f"Error: {str(e)}"
    
    def get_history(self) -> list:
        """Get calculation history."""
        return self.history


# ============================================================================
# Modern Calculator GUI
# ============================================================================

class CalculatorGUI:
    """Modern calculator interface with tkinter."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("500x750")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg_dark"])
        
        # Set custom fonts
        self.display_font = font.Font(family="Courier New", size=28, weight="bold")
        self.history_font = font.Font(family="Arial", size=10)
        self.button_font = font.Font(family="Arial", size=16, weight="bold")
        
        self.calculator = Calculator()
        self.current_display = ""
        
        self.setup_ui()
        self.bind_keyboard()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Calculator",
            font=font.Font(family="Arial", size=20, weight="bold"),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_primary"]
        )
        title_label.pack(pady=(0, 10))
        
        # Display frame
        display_frame = tk.Frame(main_frame, bg=COLORS["display_bg"], relief=tk.SUNKEN, bd=2)
        display_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 10))
        
        # History display
        self.history_label = tk.Label(
            display_frame,
            text="",
            font=self.history_font,
            bg=COLORS["display_bg"],
            fg=COLORS["history_text"],
            anchor="e",
            justify="right"
        )
        self.history_label.pack(fill=tk.X, padx=10, pady=(5, 0))
        
        # Main display
        self.display_label = tk.Label(
            display_frame,
            text="0",
            font=self.display_font,
            bg=COLORS["display_bg"],
            fg=COLORS["display_text"],
            anchor="e",
            justify="right"
        )
        self.display_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=COLORS["bg_dark"])
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button layout
        buttons = [
            ["C", "←", "÷", "×"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", "."],
            ["0", "^", "=", "√"],
        ]
        
        self.button_widgets = {}
        
        for row_idx, row in enumerate(buttons):
            row_frame = tk.Frame(button_frame, bg=COLORS["bg_dark"])
            row_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            
            for col_idx, btn_text in enumerate(row):
                self.create_button(row_frame, btn_text, col_idx, row_idx)
    
    def create_button(self, parent: tk.Frame, text: str, col: int, row: int):
        """Create a button with styling and hover effects."""
        # Determine button type and colors
        if text == "C":
            bg_color = COLORS["button_clear"]
            hover_color = COLORS["button_clear_hover"]
        elif text == "=":
            bg_color = COLORS["button_equals"]
            hover_color = COLORS["button_equals_hover"]
        elif text in ["÷", "×", "-", "+", ".", "^", "√", "←"]:
            bg_color = COLORS["button_operator"]
            hover_color = COLORS["button_operator_hover"]
        else:
            bg_color = COLORS["button_number"]
            hover_color = COLORS["button_number_hover"]
        
        # Create button
        btn = tk.Button(
            parent,
            text=text,
            font=self.button_font,
            bg=bg_color,
            fg=COLORS["text_primary"],
            border=0,
            relief=tk.RAISED,
            activebackground=hover_color,
            activeforeground=COLORS["text_primary"],
            command=lambda: self.on_button_click(text),
            cursor="hand2",
            bd=2,
            highlightthickness=0
        )
        
        btn.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5)
        
        # Store button reference
        self.button_widgets[text] = btn
        
        # Bind hover effects
        btn.bind("<Enter>", lambda e: self.on_button_enter(btn, hover_color, text))
        btn.bind("<Leave>", lambda e: self.on_button_leave(btn, bg_color, text))
    
    def on_button_enter(self, btn: tk.Button, hover_color: str, text: str):
        """Handle button hover enter."""
        btn.config(bg=hover_color)
    
    def on_button_leave(self, btn: tk.Button, bg_color: str, text: str):
        """Handle button hover leave."""
        btn.config(bg=bg_color)
    
    def on_button_click(self, char: str):
        """Handle button click."""
        if char == "C":
            self.calculator.clear()
            self.current_display = ""
        elif char == "←":
            self.calculator.backspace()
            self.current_display = self.calculator.expression
        elif char == "=":
            result = self.calculator.calculate()
            self.current_display = result
            self.update_history()
        elif char == "√":
            try:
                result = eval(self.calculator.expression)
                result = math.sqrt(result)
                self.calculator.expression = str(result)
                self.current_display = self.calculator.expression
            except Exception as e:
                self.current_display = "Error"
        elif char == "÷":
            self.calculator.add_character("/")
            self.current_display = self.calculator.expression
        elif char == "×":
            self.calculator.add_character("*")
            self.current_display = self.calculator.expression
        elif char == "^":
            self.calculator.add_character("**")
            self.current_display = self.calculator.expression
        else:
            self.calculator.add_character(char)
            self.current_display = self.calculator.expression
        
        self.update_display()
    
    def update_display(self):
        """Update the display label."""
        display_text = self.current_display if self.current_display else "0"
        
        # Limit display length
        if len(display_text) > 20:
            display_text = display_text[-20:]
        
        self.display_label.config(text=display_text)
    
    def update_history(self):
        """Update the history display."""
        if self.calculator.history:
            last_calc = self.calculator.history[-1]
            self.history_label.config(text=last_calc)
    
    def bind_keyboard(self):
        """Bind keyboard events."""
        self.root.bind("<Key>", self.on_key_press)
    
    def on_key_press(self, event: tk.Event):
        """Handle keyboard input."""
        key = event.char
        keysym = event.keysym
        
        if key.isdigit() or key in ".":
            self.on_button_click(key)
        elif key in "+-*/" or keysym == "slash":
            if keysym == "slash":
                self.on_button_click("÷")
            else:
                if key == "*":
                    self.on_button_click("×")
                else:
                    self.on_button_click(key)
        elif keysym == "Return":
            self.on_button_click("=")
        elif keysym == "BackSpace":
            self.on_button_click("←")
        elif keysym == "Escape":
            self.on_button_click("C")
        elif key.lower() == "s":
            self.on_button_click("√")
        elif key == "^":
            self.on_button_click("^")


# ============================================================================
# Main
# ============================================================================

def main():
    """Run the calculator application."""
    root = tk.Tk()
    gui = CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
