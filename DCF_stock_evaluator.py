import yfinance as yf
import my_stocks_manager as stock_manager
# This script performs a DCF valuation for a given stock ticker.
# It calculates the fair value per share based on user inputs for FCF, WACC, and growth rate. 

# === INPUT SECTION ===
personal_stocks = stock_manager.load_stocks(stock_manager.FILE_NAMES["personal"])
watchlist_stocks = stock_manager.load_stocks(stock_manager.FILE_NAMES["watchlist"])
print("=== Personal Stocks ===")
for stock in personal_stocks:
    print(f"{stock['ticker']} - Avg Price: ${stock['avg_price']:.2f}") 
print("\n=== Watchlist Stocks ===")
for stock in watchlist_stocks:
    print(stock)


# Select a stock from personal stocks or watchlist
print("\nSelect a stock for DCF valuation:")

ticker_symbol = input("Enter the stock ticker symbol (e.g., AAPL, GOOGL): ").strip().upper()
yfstock = yf.Ticker(ticker_symbol)

# Optional: Override with manual values if needed
shares_outstanding = yfstock.info.get("sharesOutstanding", 0)
net_cash = yfstock.info.get("totalCash", 0) - yfstock.info.get("totalDebt", 0)
eps_forward = yfstock.info.get("forwardEps", 0)

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
