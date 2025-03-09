from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mortgage', methods=['GET', 'POST'])
def mortgage():
    if request.method == 'POST':
        # Get form data
        principal = float(request.form.get('principal', 300000))
        down_payment = float(request.form.get('down_payment', 60000))
        interest_rate = float(request.form.get('interest', 4.5))
        term = int(request.form.get('term', 30))
        tax = float(request.form.get('tax', 3600))
        insurance = float(request.form.get('insurance', 1200))

        # Calculate loan details
        loan_amount = principal - down_payment
        monthly_rate = interest_rate / 100 / 12
        num_payments = term * 12
        
        # Calculate monthly payment
        monthly_payment = (loan_amount * monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        monthly_tax = tax / 12
        monthly_insurance = insurance / 12
        total_monthly = monthly_payment + monthly_tax + monthly_insurance

        # Generate amortization schedule
        amortization = []
        remaining_balance = loan_amount
        total_interest = 0

        for payment_num in range(1, num_payments + 1):
            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            total_interest += interest_payment
            
            amortization.append({
                'payment_num': payment_num,
                'payment_date': (datetime.now().replace(day=1) + pd.DateOffset(months=payment_num)).strftime('%Y-%m-%d'),
                'monthly_payment': monthly_payment,
                'principal_payment': principal_payment,
                'interest_payment': interest_payment,
                'remaining_balance': remaining_balance,
                'total_interest': total_interest
            })

        # Create payment breakdown graph
        fig, ax = plt.subplots(figsize=(10, 6))
        years = np.arange(term + 1)
        principal_data = [loan_amount * (1 - (1 + monthly_rate)**(year * 12)) / (1 - (1 + monthly_rate)**num_payments) for year in years]
        interest_data = [monthly_payment * year * 12 - (loan_amount - loan_amount * (1 - (1 + monthly_rate)**(year * 12)) / (1 - (1 + monthly_rate)**num_payments)) for year in years]

        ax.stackplot(years, [principal_data, interest_data], labels=['Principal', 'Interest'])
        ax.set_xlabel('Years')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Mortgage Payment Breakdown Over Time')
        ax.legend()
        ax.grid(True)

        # Convert plot to base64 string
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()

        return render_template('mortgage.html', 
                             monthly_payment=monthly_payment,
                             monthly_tax=monthly_tax,
                             monthly_insurance=monthly_insurance,
                             total_monthly=total_monthly,
                             amortization=amortization,
                             plot_url=plot_url)

    return render_template('mortgage.html')

@app.route('/investment')
def investment():
    return render_template('investment.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

if __name__ == '__main__':
    app.run(debug=True, port=5555)