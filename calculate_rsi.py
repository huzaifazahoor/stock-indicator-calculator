import pandas as pd

from utils import update_indicator_in_db


def calculate_rsi(data, window=14):
    """
    Calculates the Relative Strength Index (RSI) for a given stock data.

    Parameters:
    data (DataFrame): Pandas DataFrame containing the stock data with a 'Close' column.
    window (int): The window size for calculating RSI. Defaults to 14.

    Returns:
    data (DataFrame): Pandas DataFrame with an added 'RSI' column containing the calculated RSI values.
    """
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data["RSI"] = rsi
    return data


def fetch_and_calculate_indicator(
    collection,
    ticker,
    start_date,
    indicator_func,
    indicator_name,
):
    """
    Fetches stock data from MongoDB and calculates the specified indicator for the fetched data.
    Updates the database with the latest indicator value and the corresponding date.

    Parameters:
    collection (Collection): MongoDB collection from which to fetch the data.
    ticker (str): Stock ticker symbol.
    start_date (datetime): The start date from which to fetch the data.
    indicator_func (function): The function to calculate the indicator.
    indicator_name (str): The name of the indicator.

    Returns:
    data (DataFrame): Pandas DataFrame containing the fetched stock data with the calculated indicator.
    """
    data = pd.DataFrame(
        list(collection.find({"Ticker": ticker, "Date": {"$gte": start_date}}))
    )

    data.sort_values(by="Date", inplace=True)
    data = indicator_func(data)

    # Extract the latest indicator value and date
    latest_indicator = data[["Date", indicator_name]].iloc[-1]

    # Update the database with the latest indicator value
    update_indicator_in_db(
        collection,
        ticker,
        indicator_name,
        latest_indicator[indicator_name],
        latest_indicator["Date"],
    )

    return data
