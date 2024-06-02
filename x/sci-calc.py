import tkinter as tk
from math import *

def calculate():
    try:
        expression = entry.get()
        expression = expression.replace("^", "**")  # Replace ^ with ** for exponentiation
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def clear():
    entry.delete(0, tk.END)

def button_click(symbol):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + symbol)

def create_calc_window():
    calc_window = tk.Tk()
    calc_window.title("Scientific Calculator")
    
    global entry
    entry = tk.Entry(calc_window, width=40, borderwidth=5)
    entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    buttons = [
        ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
        ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
        ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
        ("0", 4, 0), (".", 4, 1), ("+", 4, 2), ("^", 4, 3),  # Moved ^ next to +
        ("sin", 5, 0), ("cos", 5, 1), ("tan", 5, 2), ("clr", 5, 3),  # Moved clr next to tan
        ("(", 6, 0), (")", 6, 1), ("sqrt", 6, 2), ("=", 6, 3)  # Moved = next to sqrt
    ]

    for button in buttons:
        symbol, row, col = button
        if symbol == "=":
            btn = tk.Button(calc_window, text=symbol, padx=20, pady=10, command=calculate)
        elif symbol == "clr":
            btn = tk.Button(calc_window, text=symbol, padx=15, pady=10, command=clear)
        else:
            btn = tk.Button(calc_window, text=symbol, padx=20, pady=10, command=lambda s=symbol: button_click(s))
        btn.grid(row=row, column=col, padx=5, pady=5)

create_calc_window()
tk.mainloop()

