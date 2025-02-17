from flask import Flask, request, jsonify, render_template
import yfinance as yf
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# --- Configuration (Ticker and Date Range - can be globals) ---
ticker = "^GSPC"
start_date = "1948-07-01"
end_date = "2024-07-01"
default_withdrawal_rate = 0.04  # Default withdrawal rate: 4%

default_csv_filename = 'sp500_monte_carlo_ending_assets_deciles_withdrawal.csv' # Set default filename

def monte_carlo_simulation(num_years, num_sims, initial_investment, withdrawal_rate=default_withdrawal_rate, output_file_path=None):
    """
    Performs Monte Carlo simulation with annual withdrawals, using 100-year historical S&P 500 returns.
    Calculates distribution of ending asset values by decile after withdrawals, saves to CSV, and returns summary statistics.

    Args:
        num_years (int): Number of years to simulate.
        num_sims (int): Number of simulations to run.
        initial_investment (float or int): The starting investment amount.
        withdrawal_rate (float, optional): Annual withdrawal rate (percentage as a decimal, e.g., 0.04 for 4%). Defaults to default_withdrawal_rate (4%).
        output_file_path (str, optional): Full path (including filename) to save the percentile CSV.
                                          If None, it will save to 'sp500_monte_carlo_ending_assets_deciles_withdrawal.csv' in the current directory.

    Returns:
        tuple: (average_cumulative_return_factor, average_annualized_return_percent, percentile_df)
               - average_cumulative_return_factor (float): Average cumulative return factor at end of simulation.
               - average_annualized_return_percent (float): Approximate average annualized return (before withdrawals are factored into annualized return calculation).
               - percentile_df (pd.DataFrame): DataFrame containing decile data for ENDING ASSET VALUES (Deciles of Ending Assets after withdrawals).
    """
    # --- 1. Fetch Historical S&P 500 Annual Returns (NOW INSIDE FUNCTION) ---
    sp500_data = yf.download(ticker, start=start_date, end=end_date)
    annual_prices = sp500_data[('Close', '^GSPC')].resample('YE').last()
    historical_annual_returns = annual_prices.pct_change().dropna()
    historical_annual_returns_list = historical_annual_returns.tolist() # Convert to list

    all_ending_asset_values = [] # List to store ending asset values for all simulations
    all_cumulative_returns_by_year = [] # Still storing cumulative returns for summary stats (before withdrawals)

    for _ in range(num_sims):
        simulated_returns = np.random.choice(historical_annual_returns_list, size=num_years, replace=True)
        cumulative_returns_path = [] # Store cumulative returns for each year in this simulation
        cumulative_return_factor = 1.0 # Start with a return factor of 1 (initial value)

        for annual_return in simulated_returns:
            cumulative_return_factor *= (1 + annual_return) # Update cumulative return factor year by year
            withdrawal_amount = initial_investment * cumulative_return_factor * withdrawal_rate # Calculate withdrawal amount based on current value
            cumulative_return_factor -= withdrawal_rate # Apply withdrawal as percentage *before* next year's return (incorrect logic)
            cumulative_returns_path.append(cumulative_return_factor) # Store cumulative return at end of each year


        all_cumulative_returns_by_year.append(cumulative_returns_path) # Add this simulation's year-by-year returns

        ending_asset_value = initial_investment * cumulative_return_factor # Calculate ending asset value
        all_ending_asset_values.append(ending_asset_value) # Store ending asset value

    # --- Calculate Percentiles (Deciles) for Ending Asset Values ---
    decile_values = np.percentile(all_ending_asset_values, [10, 20, 30, 40, 50, 60, 70, 80, 90]) # Decile percentiles

    percentile_data = [{
        'Decile': '10th',
        'Ending Asset Value': decile_values[0]
    }, {
        'Decile': '20th',
        'Ending Asset Value': decile_values[1]
    }, {
        'Decile': '30th',
        'Ending Asset Value': decile_values[2]
    }, {
        'Decile': '40th',
        'Ending Asset Value': decile_values[3]
    }, {
        'Decile': '50th (Median)',
        'Ending Asset Value': decile_values[4]
    }, {
        'Decile': '60th',
        'Ending Asset Value': decile_values[5]
    }, {
        'Decile': '70th',
        'Ending Asset Value': decile_values[6]
    }, {
        'Decile': '80th',
        'Ending Asset Value': decile_values[7]
    }, {
        'Decile': '90th',
        'Ending Asset Value': decile_values[8]
    }]

    percentile_df = pd.DataFrame(percentile_data)
    percentile_df['Ending Asset Value'] = percentile_df['Ending Asset Value'].round(2) # Round asset values

    # --- Determine output CSV path ---
    if output_file_path is None:
        output_file_path = default_csv_filename # Default filename

    # --- Save Percentile Data to CSV ---
    percentile_df.to_csv(output_file_path, index=False)
    print(f"Percentile data saved to: {output_file_path}") # Confirmation message

    # --- Calculate Summary Statistics (Cumulative Return - unchanged, Annualized Return now less relevant with withdrawals) ---
    average_cumulative_return_factor_at_end = np.mean([sim_returns[-1] for sim_returns in all_cumulative_returns_by_year]) # Average of cumulative returns at the end of simulation_years (BEFORE WITHDRAWALS are directly factored in for annualized return)
    average_annualized_return_percent = (average_cumulative_return_factor_at_end**(1/num_years) - 1) * 100 # Approximate annualized return (BEFORE WITHDRAWALS are directly factored in)

    return average_cumulative_return_factor_at_end, average_annualized_return_percent, percentile_df


@app.route('/') # <--- NOW @app.route will work because 'app' is already defined
def index():
    print("Current Working Directory:", os.getcwd()) # Debug prints (keep these for now)
    template_folder = os.path.join(app.root_path, app.template_folder)
    print("Template Folder Path:", template_folder)
    print("Templates Folder Exists:", os.path.exists(template_folder))
    print("index.html Exists in Templates:", os.path.exists(os.path.join(template_folder, 'index.html')))
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    num_years = int(request.form['num_years'])
    num_sims = int(request.form['num_sims'])
    initial_investment = float(request.form['initial_investment'])
    withdrawal_rate = float(request.form['withdrawal_rate']) / 100.0  # Convert percentage to decimal

    avg_cum_return, avg_annual_return, percentile_df = monte_carlo_simulation(
        num_years=num_years,
        num_sims=num_sims,
        initial_investment=initial_investment,
        withdrawal_rate=withdrawal_rate
    )

    decile_data = percentile_df.to_dict('records') # Convert DataFrame to list of dictionaries for JSON

    return jsonify({ # <--- This is the crucial return statement that was missing!
        'deciles': decile_data,
        'avg_cumulative_return': round(avg_cum_return, 2),
        'avg_annualized_return': round(avg_annual_return, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
