Stock Indicator Calculator
==========================

This project fetches stock data, calculates financial indicators, and updates the results in a MongoDB database. It is designed to be easily extendable to include additional indicators.

Prerequisites
-------------

-   Python 3.x
-   MongoDB
-   Required Python libraries:
    -   `yfinance`
    -   `pandas`
    -   `pymongo`

Setup
-----

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/stock-indicator-calculator.git
    cd stock-indicator-calculator
    ```

2.  **Install the required libraries:**

    ```sh
    pip install -r requirements
    ```

3.  **Set up MongoDB:**

    Make sure you have MongoDB installed and running. Create a `.env` file and update the var `PYMONGO_URI`.

Usage
-----

1.  **Run the main script:**

    ```sh
    python main.py
    ```

2.  **Follow the prompts:**

    -   Enter the stock ticker symbol (e.g., AAPL).
    -   Select the indicator to calculate (e.g., 1 for RSI).

Adding New Indicators
---------------------

To add new indicators, follow these steps:

1.  **Create a new function to calculate the indicator in the `calculate_new_indicator.py` file:**

    ```python
    def calculate_new_indicator(data, window=14):
        # Your calculation logic here
        data["New_Indicator"] = # Calculated values
        return data
    ```

2.  **Update the `main.py` file to include the new indicator:**

    ```python
    `from calculate_new_indicator import calculate_new_indicator

    def main():
        # ... existing code ...

        # Menu for selecting indicators
        print("Select the indicators to calculate:")
        print("1. RSI (Relative Strength Index)")
        print("2. New Indicator (Your new indicator name)")
        indicators = input("Enter the number of the indicator to calculate (e.g., 1): ").strip()

        # ... existing code ...

        # Calculate selected indicators
        if indicators == "1":
            data = calculate_rsi(collection, ticker, start_date, calculate_rsi, "RSI")
            print(data[["Date", "Close", "RSI"]].tail())
        elif indicators == "2":
            data = fetch_and_calculate_indicator(collection, ticker, start_date, calculate_new_indicator, "New_Indicator")
            print(data[["Date", "Close", "New_Indicator"]].tail())
        else:
            print("Invalid selection. Please enter a valid number for the indicator.")

    if __name__ == "__main__":
        main()
    ```

3.  **Run the main script and select your new indicator:**

    ```sh
    python main.py
    ```

File Structure
--------------

-   `utils.py`: Contains utility functions for database operations and fetching data from yfinance.
-   `calculate_rsi.py`: Contains functions to calculate various financial indicators.
-   `main.py`: The main script that integrates everything and provides an interactive interface.