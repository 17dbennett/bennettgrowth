import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PortfolioSimulator(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Input fields frame
        input_frame = ttk.Frame(self)
        input_frame.grid(row=0, column=0, padx=10, pady=5)

        # Portfolio allocation inputs
        tk.Label(input_frame, text="Portfolio Allocation (%)").grid(row=0, column=0, columnspan=2, pady=10)
        
        self.allocations = {}
        assets = [
            ("Stocks", 60),
            ("Bonds", 30),
            ("Cash", 10)
        ]

        for i, (asset, default) in enumerate(assets):
            tk.Label(input_frame, text=asset).grid(row=i+1, column=0, padx=5, pady=5)
            self.allocations[asset] = tk.Entry(input_frame)
            self.allocations[asset].insert(0, str(default))
            self.allocations[asset].grid(row=i+1, column=1, padx=5, pady=5)

        # Simulation parameters
        tk.Label(input_frame, text="Simulation Parameters").grid(row=len(assets)+1, column=0, columnspan=2, pady=10)
        
        self.params = {}
        parameters = [
            ("Initial Investment ($)", "initial", 100000),
            ("Time Horizon (years)", "years", 30),
            ("Number of Simulations", "sims", 1000)
        ]

        for i, (label, key, default) in enumerate(parameters):
            tk.Label(input_frame, text=label).grid(row=i+len(assets)+2, column=0, padx=5, pady=5)
            self.params[key] = tk.Entry(input_frame)
            self.params[key].insert(0, str(default))
            self.params[key].grid(row=i+len(assets)+2, column=1, padx=5, pady=5)

        # Calculate button
        tk.Button(input_frame, text="Run Simulation", command=self.simulate).grid(
            row=len(assets)+len(parameters)+2, column=0, columnspan=2, pady=10)

        # Result display
        self.result_text = tk.Text(input_frame, height=4, width=40)
        self.result_text.grid(row=len(assets)+len(parameters)+3, column=0, columnspan=2, padx=5, pady=5)

        # Graph frame
        self.graph_frame = ttk.Frame(self)
        self.graph_frame.grid(row=0, column=1, padx=10, pady=5)

    def simulate(self):
        try:
            # Get allocation values
            allocations = {asset: float(entry.get())/100 for asset, entry in self.allocations.items()}
            if sum(allocations.values()) != 1:
                raise ValueError("Allocations must sum to 100%")

            # Get simulation parameters
            initial = float(self.params["initial"].get())
            years = int(self.params["years"].get())
            n_sims = int(self.params["sims"].get())

            # Asset return assumptions (mean, std)
            returns = {
                "Stocks": (0.10, 0.15),  # 10% return, 15% volatility
                "Bonds": (0.05, 0.05),   # 5% return, 5% volatility
                "Cash": (0.02, 0.01)     # 2% return, 1% volatility
            }

            # Run Monte Carlo simulation
            monthly_returns = np.zeros((n_sims, years * 12))
            for asset, alloc in allocations.items():
                mean, std = returns[asset]
                r = np.random.normal(mean/12, std/np.sqrt(12), (n_sims, years * 12))
                monthly_returns += r * alloc

            # Calculate portfolio values
            portfolio_values = initial * np.cumprod(1 + monthly_returns, axis=1)

            # Calculate statistics
            final_values = portfolio_values[:, -1]
            median_final = np.median(final_values)
            percentile_95 = np.percentile(final_values, 95)
            percentile_5 = np.percentile(final_values, 5)

            # Display results
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, 
                f"Median Final Value: ${median_final:,.2f}\n"
                f"95th Percentile: ${percentile_95:,.2f}\n"
                f"5th Percentile: ${percentile_5:,.2f}"
            )

            # Plot results
            for widget in self.graph_frame.winfo_children():
                widget.destroy()

            fig, ax = plt.subplots(figsize=(6, 4))
            months = np.arange(years * 12 + 1) / 12
            
            # Plot all simulations with low opacity
            for sim in portfolio_values[::int(n_sims/100)]:  # Plot every 100th simulation
                ax.plot(months[1:], sim/1000, 'b-', alpha=0.1)
            
            # Plot median path
            median_path = np.median(portfolio_values, axis=0)
            ax.plot(months[1:], median_path/1000, 'r-', linewidth=2, label='Median Path')
            
            ax.set_xlabel('Years')
            ax.set_ylabel('Portfolio Value (Thousands $)')
            ax.set_title('Monte Carlo Portfolio Simulation')
            ax.grid(True)
            ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        except ValueError as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Error: {str(e)}")