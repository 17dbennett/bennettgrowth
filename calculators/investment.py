import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InvestmentCalculator(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Input fields
        self.inputs = {}
        input_fields = [
            ("Initial Investment ($)", "initial", 10000),
            ("Monthly Contribution ($)", "monthly", 500),
            ("Expected Return (%)", "return", 7),
            ("Investment Duration (years)", "duration", 20),
            ("Compound Frequency", "compound", "12")
        ]

        input_frame = ttk.Frame(self)
        input_frame.grid(row=0, column=0, padx=10, pady=5)

        for i, (label, key, default) in enumerate(input_fields):
            tk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
            self.inputs[key] = tk.Entry(input_frame)
            self.inputs[key].insert(0, str(default))
            self.inputs[key].grid(row=i, column=1, padx=5, pady=5)

        # Calculate button
        tk.Button(input_frame, text="Calculate", command=self.calculate).grid(row=len(input_fields), column=0, columnspan=2, pady=10)

        # Result display
        self.result_text = tk.Text(input_frame, height=4, width=40)
        self.result_text.grid(row=len(input_fields)+1, column=0, columnspan=2, padx=5, pady=5)

        # Graph frame
        self.graph_frame = ttk.Frame(self)
        self.graph_frame.grid(row=0, column=1, padx=10, pady=5)

    def calculate(self):
        try:
            # Get values from inputs
            P = float(self.inputs["initial"].get())
            PMT = float(self.inputs["monthly"].get())
            r = float(self.inputs["return"].get()) / 100
            t = int(self.inputs["duration"].get())
            n = int(self.inputs["compound"].get())

            # Calculate growth over time
            months = np.arange(0, t * 12 + 1)
            r_monthly = r / 12
            balance = P * (1 + r_monthly)**(months) + PMT * ((1 + r_monthly)**(months) - 1) / r_monthly

            # Calculate final amount
            final_amount = balance[-1]
            total_contributions = P + PMT * t * 12
            total_earnings = final_amount - total_contributions

            # Display results
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, 
                f"Final Amount: ${final_amount:,.2f}\n"
                f"Total Contributions: ${total_contributions:,.2f}\n"
                f"Total Earnings: ${total_earnings:,.2f}\n"
                f"Return on Investment: {(total_earnings/total_contributions)*100:.1f}%"
            )

            # Plot graph
            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(months/12, balance/1000, 'b-')
            ax.set_xlabel('Years')
            ax.set_ylabel('Amount (Thousands $)')
            ax.set_title('Investment Growth Over Time')
            ax.grid(True)

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        except ValueError:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please enter valid numbers for all fields")