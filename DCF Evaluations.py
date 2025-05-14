import yfinance as yf
import requests

# === ALPHA VANTAGE API KEY ===
api_key = 'your_alpha_vantage_api_key_here'  # Replace with your API Key

# === INPUT SECTION ===
ticker_symbol = input("Enter stock ticker (e.g., AAPL, GOOGL): ").upper()
stock = yf.Ticker(ticker_symbol)

# Optional: Override with manual values if needed
shares_outstanding = stock.info.get("sharesOutstanding", 0)
net_cash = stock.info.get("totalCash", 0) - stock.info.get("totalDebt", 0)
eps_forward = stock.info.get("forwardEps", 0)

# === ALPHA VANTAGE API: Fetch Segment Data ===
def get_alpha_vantage_data(ticker):
    url = f'https://www.alphavantage.co/query'
    params = {
        'function': 'OVERVIEW',
        'symbol': ticker,
        'apikey': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract relevant data
    try:
        print(f"\n--- Segment and Overview Data from Alpha Vantage ---")
        print(f"Company: {data.get('Name', 'N/A')}")
        print(f"Industry: {data.get('Industry', 'N/A')}")
        print(f"Description: {data.get('Description', 'N/A')}")
        print(f"Sector: {data.get('Sector', 'N/A')}")
        print(f"Market Capitalization: {data.get('MarketCapitalization', 'N/A')}")
        print(f"Revenue (ttm): {data.get('RevenueTTM', 'N/A')}")
    except KeyError:
        print(f"Error: Could not fetch data for {ticker}. Ensure the ticker is correct or data is available.")

# === RELATIVE VALUATION (PE Multiples) ===
current_pe = stock.info.get("trailingPE", 0)

print("\n--- Relative Valuation ---")
if current_pe != 0:
    pe_multiples = {
        'Bear Case': current_pe - 5,
        'Base Case': current_pe,
        'Bull Case': current_pe + 5
    }

    for label, pe in pe_multiples.items():
        fair_value = pe * eps_forward
        print(f"{label} (P/E {pe}): ${fair_value:.2f}")
else:
    print("Current P/E data not available for this stock.")

# === DCF VALUATION ===
# Example: manual 5-year FCF forecast
fcf_list = [float(input(f"Enter Year {i+1} FCF ($B): ")) * 1e9 for i in range(5)]
wacc = float(input("Enter WACC (e.g., 0.085 for 8.5%): "))
g = float(input("Enter terminal growth rate (e.g., 0.03 for 3%): "))

pv_fcf = [fcf / (1 + wacc)**(i+1) for i, fcf in enumerate(fcf_list)]
terminal_value = fcf_list[-1] * (1 + g) / (wacc - g)
pv_terminal = terminal_value / (1 + wacc)**5
enterprise_value = sum(pv_fcf) + pv_terminal
equity_value = enterprise_value + net_cash
fair_value_per_share_dcf = equity_value / shares_outstanding

print("\n--- DCF Valuation ---")
print(f"Fair Value per Share (DCF): ${fair_value_per_share_dcf:.2f}")

# === SOTP VALUATION (manual inputs) ===
print("\n--- SOTP Valuation ---")
sotp_segments = {}
while True:
    segment = input("Enter segment name (or 'done' to finish): ")
    if segment.lower() == "done":
        break
    value = float(input(f"Enter value of {segment} ($B): ")) * 1e9
    sotp_segments[segment] = value

sotp_total_value = sum(sotp_segments.values()) + net_cash
fair_value_per_share_sotp = sotp_total_value / shares_outstanding

print(f"\nTotal SOTP Value: ${sotp_total_value / 1e9:.2f}B")
print(f"Fair Value per Share (SOTP): ${fair_value_per_share_sotp:.2f}")

# === Fetching Alpha Vantage Data ===
get_alpha_vantage_data(ticker_symbol)
