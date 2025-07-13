import yfinance as yf

# === INPUT SECTION ===
ticker_symbol = input("Enter stock ticker (e.g., AAPL, GOOGL): ").upper()
stock = yf.Ticker(ticker_symbol)

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