import csv
import sys # Used for clean exit if no stocks are entered

# --- Hardcoded Stock Prices Dictionary ---
# These prices are updated to reflect a more diverse and realistic example portfolio
# across various industries (Tech, Healthcare, Finance, Retail).
STOCK_PRICES = {
    "NVDA": 875.50,  # NVIDIA Corporation (High-growth Tech)
    "JNJ": 158.30,   # Johnson & Johnson (Healthcare/Staple)
    "V": 270.15,     # Visa Inc. (Financial Technology)
    "COST": 780.00,  # Costco Wholesale Corporation (Retail/Staple)
    "ASML": 995.88,  # ASML Holding N.V. (Global Semiconductor Equipment)
    "RY": 105.45     # Royal Bank of Canada (Canadian Finance)
}

def get_user_portfolio():
    """
    Prompts the user to input stock tickers and quantities.
    Validates input and ensures the ticker exists in STOCK_PRICES.
    Returns a list of dictionaries, where each dictionary represents a holding.
    """
    portfolio = []
    print("\n--- Enter Your Stock Holdings ---")
    print(f"Available stocks: {', '.join(STOCK_PRICES.keys())}")
    print("Type 'done' when you have finished entering your stocks.")

    while True:
        ticker = input("Enter stock ticker (e.g., NVDA): ").strip().upper()
        if ticker == 'DONE':
            break

        # Check if the ticker is valid
        if ticker not in STOCK_PRICES:
            print(f"Error: Stock '{ticker}' not found in the price list. Please try one of the available options.")
            continue

        # Get and validate quantity
        while True:
            try:
                quantity_input = input(f"Enter quantity for {ticker}: ").strip()
                if not quantity_input:
                    print("Quantity cannot be empty.")
                    continue
                quantity = int(quantity_input)
                if quantity <= 0:
                    print("Quantity must be a positive whole number.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a whole number for quantity.")

        # Calculate the value of the holding
        price = STOCK_PRICES[ticker]
        value = quantity * price

        portfolio.append({
            'ticker': ticker,
            'quantity': quantity,
            'price': price,
            'value': value,
            'weight': 0.0  # Initialize weight to be calculated later
        })
        print(f"-> Added {quantity} shares of {ticker} at ${price:.2f} each. Current value: ${value:,.2f}")

    return portfolio

def calculate_portfolio_value(portfolio):
    """
    Calculates the total market value of the portfolio from the list of holdings.
    Returns the total value (float).
    """
    total_value = sum(holding['value'] for holding in portfolio)
    return total_value

def calculate_portfolio_weights(portfolio, total_value):
    """
    Calculates the percentage weight of each stock holding relative to the total portfolio value.
    Updates the 'weight' key in each holding dictionary in the portfolio list.
    """
    # Defensive check to avoid division by zero
    if total_value == 0:
        return

    for holding in portfolio:
        # Calculate percentage weight
        weight = (holding['value'] / total_value) * 100
        holding['weight'] = weight

def save_results_to_file(portfolio, total_value, filename="portfolio_summary.txt"):
    """
    Saves the detailed portfolio report, including weight, and total value to a plain text file.
    """
    try:
        with open(filename, 'w') as f:
            f.write("=" * 65 + "\n")
            f.write("     STOCK PORTFOLIO SUMMARY\n")
            f.write("=" * 65 + "\n")
            # Increased width for the new column
            f.write(f"{'Ticker':<10}{'Quantity':<10}{'Price':<10}{'Value (USD)':<15}{'Weight (%)':<15}\n")
            f.write("-" * 65 + "\n")

            for holding in portfolio:
                # Added weight column formatting
                f.write(f"{holding['ticker']:<10}{holding['quantity']:<10}{holding['price']:<10.2f}{holding['value']:<15.2f}{holding['weight']:<15.2f}\n")

            f.write("-" * 65 + "\n")
            f.write(f"Total Investment Value: ${total_value:,.2f}\n")
            f.write("=" * 65 + "\n")

        print(f"\n[SUCCESS] Report successfully saved to {filename}")

    except IOError as e:
        print(f"\n[ERROR] An error occurred while saving the file: {e}")

def main():
    """
    Main execution function.
    """
    print("<<< Welcome to the Simple Stock Portfolio Tracker >>>")

    # 1. Get user input
    user_portfolio = get_user_portfolio()

    if not user_portfolio:
        print("\nNo stocks were entered. Application closing.")
        sys.exit() # Exit cleanly if no data was entered

    # 2. Calculate total value
    total_value = calculate_portfolio_value(user_portfolio)
    
    # 3. Calculate portfolio weights (the new feature)
    calculate_portfolio_weights(user_portfolio, total_value)

    # 4. Display results
    print("\n" + "=" * 65) # Adjusted width
    print("     FINAL PORTFOLIO REPORT    ")
    print("=" * 65) # Adjusted width
    # Added 'Weight (%)' to the header
    print(f"{'Ticker':<10}{'Quantity':<10}{'Price':<10}{'Value (USD)':<15}{'Weight (%)':<15}")
    print("-" * 65) # Adjusted width
    for holding in user_portfolio:
        # Added weight column formatting
        print(f"{holding['ticker']:<10}{holding['quantity']:<10}{holding['price']:<10.2f}{holding['value']:<15.2f}{holding['weight']:<15.2f}")
    print("-" * 65) # Adjusted width
    print(f"Total Portfolio Value: ${total_value:,.2f}")
    print("=" * 65) # Adjusted width

    # 5. Optional File Handling
    save_option = input("\nDo you want to save this report to a file (portfolio_summary.txt)? (y/n): ").strip().lower()
    if save_option == 'y':
        save_results_to_file(user_portfolio, total_value)
    else:
        print("File saving skipped.")

if __name__ == "__main__":
    main()
