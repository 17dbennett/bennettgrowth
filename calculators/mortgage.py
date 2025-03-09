import tkinter as tk
from tkinter import ttk
import numpy as np

class MortgageCalculator(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Input fields
        self.inputs = {}
        input_fields = [
            ("Principal ($)", "principal", 300000),
            ("Interest Rate (%)", "interest", 4.5),
            ("Loan Term (years)", "term", 30),
            ("Down Payment ($)", "down_payment", 60000),
            ("Property Tax ($/year)", "tax", 3600),
            ("Insurance ($/year)", "insurance", 1200)
        ]

        for i, (label, key, default) in enumerate(input_fields):
            tk.Label(self, text=label).grid(row=i, column=0, padx=5, pady=5)
            self.inputs[key] = tk.Entry(self)
            self.inputs[key].insert(0, str(default))
            self.inputs[key].grid(row=i, column=1, padx=5, pady=5)

        # Calculate button
        tk.Button(self, text="Calculate", command=self.calculate).grid(row=len(input_fields), column=0, columnspan=2, pady=10)

        # Result display
        self.result_text = tk.Text(self, height=4, width=40)
        self.result_text.grid(row=len(input_fields)+1, column=0, columnspan=2, padx=5, pady=5)

    def calculate(self):
        try:
            # Get values from inputs
            P = float(self.inputs["principal"].get()) - float(self.inputs["down_payment"].get())
            r = float(self.inputs["interest"].get()) / 100 / 12
            n = int(self.inputs["term"].get()) * 12
            tax = float(self.inputs["tax"].get()) / 12
            insurance = float(self.inputs["insurance"].get()) / 12

            # Calculate monthly mortgage payment
            monthly_payment = (P * r * (1 + r)**n) / ((1 + r)**n - 1)
            total_monthly = monthly_payment + tax + insurance

            # Display results
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, 
                f"Monthly Principal & Interest: ${monthly_payment:,.2f}\n"
                f"Monthly Tax: ${tax:,.2f}\n"
                f"Monthly Insurance: ${insurance:,.2f}\n"
                f"Total Monthly Payment: ${total_monthly:,.2f}"
            )

        except ValueError:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please enter valid numbers for all fields")