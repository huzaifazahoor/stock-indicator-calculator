from datetime import datetime, timedelta

from calculate_rsi import calculate_rsi, fetch_and_calculate_indicator
from utils import (
    fetch_data_from_db,
    fetch_data_from_yfinance,
    get_db_connection,
    update_db,
)


def main():
    # Connect to MongoDB
    db = get_db_connection()
    collection = db["historical_prices"]

    # User input for ticker
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ").strip().upper()

    # Menu for selecting indicators
    print("Select the indicators to calculate:")
    print("1. RSI (Relative Strength Index)")
    indicators = input(
        "Enter the number of the indicator to calculate (e.g., 1): "
    ).strip()

    # Parameters
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)

    # Fetch data from DB
    data = fetch_data_from_db(collection, ticker, start_date)

    # Fetch from yfinance if data is missing
    if data.empty:
        data = fetch_data_from_yfinance(ticker)
        update_db(collection, data)

    # Calculate selected indicators
    if indicators == "1":
        data = fetch_and_calculate_indicator(
            collection,
            ticker,
            start_date,
            calculate_rsi,
            "RSI",
        )
        print(data[["Date", "Close", "RSI"]].tail())
    else:
        print("Invalid selection. Please enter a valid number for the indicator.")


if __name__ == "__main__":
    main()
