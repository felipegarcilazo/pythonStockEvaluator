# stock_manager.py

import os
import json
import yfinance as yf

FILE_NAMES = {
    "personal": "personal_stocks.json",
    "watchlist": "watchlist_stocks.json"
}

def load_stocks(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    return []

def save_stocks(file_name, stocks):
    with open(file_name, "w") as file:
        json.dump(stocks, file, indent=4)

def is_valid_ticker(ticker):
    ticker = ticker.upper()
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return bool(info.get("shortName"))
    except Exception:
        return False

def stock_exists(ticker, stock_list):
    return any(stock["ticker"] == ticker for stock in stock_list)

def add_stock(stock_list, new_stock, list_type):
    new_stock = new_stock.upper()

    if list_type == "personal":
        if stock_exists(new_stock, stock_list):
            print(f"{new_stock} is already in your personal stock list.")
            return

        if is_valid_ticker(new_stock):
            try:
                avg_price = float(input(f"Enter average price paid for {new_stock}: ").strip())
                stock_list.append({"ticker": new_stock, "avg_price": avg_price})
                print(f"{new_stock} added with average price ${avg_price:.2f}.")
            except ValueError:
                print("Invalid price input.")
        else:
            print(f"{new_stock} is not a valid stock ticker.")
    else:
        if new_stock in stock_list:
            print(f"{new_stock} is already in the watchlist.")
            return

        if is_valid_ticker(new_stock):
            stock_list.append(new_stock)
            print(f"{new_stock} added to watchlist.")
        else:
            print(f"{new_stock} is not a valid stock ticker.")

def manage_stocks(list_type):
    file_name = FILE_NAMES[list_type]
    stocks = load_stocks(file_name)
    print(f"\nManaging {list_type} stock list.")

    while True:
        print("\nOptions:")
        print("1. Add a stock")
        print("2. Exit")
        action = input("Enter your choice: ").strip()

        if action == "1":
            ticker = input("Enter stock ticker to add: ").strip()
            add_stock(stocks, ticker, list_type)
        elif action == "2":
            break
        else:
            print("Invalid option.")

    save_stocks(file_name, stocks)
    print(f"{list_type.capitalize()} stock list saved.")