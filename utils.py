import os

import pandas as pd
import yfinance as yf
from pymongo import MongoClient


def get_db_connection(uri=os.getenv("PYMONGO_URI")):
    """
    Establishes a connection to the MongoDB database.

    Parameters:
    uri (str): MongoDB connection URI. Defaults to environment variable PYMONGO_URI.

    Returns:
    db (Database): MongoDB database connection.
    """
    client = MongoClient(uri)
    db = client["stock_data"]
    return db


def fetch_data_from_db(collection, ticker, start_date):
    """
    Fetches stock data from MongoDB starting from a specified date.

    Parameters:
    collection (Collection): MongoDB collection from which to fetch the data.
    ticker (str): Stock ticker symbol.
    start_date (datetime): The start date from which to fetch the data.

    Returns:
    data (DataFrame): Pandas DataFrame containing the fetched stock data.
    """
    data = pd.DataFrame(
        list(collection.find({"Ticker": ticker, "Date": {"$gte": start_date}}))
    )
    return data


def update_db(collection, data):
    """
    Updates the MongoDB collection with new stock data.

    Parameters:
    collection (Collection): MongoDB collection to be updated.
    data (DataFrame): Pandas DataFrame containing the stock data to be inserted.

    Returns:
    None
    """
    data_dict = data.to_dict("records")
    collection.insert_many(data_dict)


def fetch_data_from_yfinance(ticker, period="1y"):
    """
    Fetches stock data from yfinance for a specified period.

    Parameters:
    ticker (str): Stock ticker symbol.
    period (str): Period for which to fetch the data (e.g., '1y' for one year). Defaults to '1y'.

    Returns:
    hist (DataFrame): Pandas DataFrame containing the fetched stock data.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    hist.reset_index(inplace=True)
    hist["Ticker"] = ticker
    return hist


def update_indicator_in_db(collection, ticker, indicator_name, indicator_value, date):
    """
    Updates the MongoDB collection with the latest indicator value.

    Parameters:
    collection (Collection): MongoDB collection to be updated.
    ticker (str): Stock ticker symbol.
    indicator_name (str): The name of the indicator to be updated.
    indicator_value (float): The latest value of the indicator.
    date (datetime): The date of the latest indicator value.

    Returns:
    None
    """
    print("updatin")
    collection.update_one(
        {"Ticker": ticker},
        {
            "$set": {
                f"Latest_{indicator_name}": indicator_value,
                f"{indicator_name}_Date": date,
            }
        },
        upsert=True,
    )
