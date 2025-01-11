import requests
from decouple import config

ALPHA_VANTAGE_API_KEY = config("ALPHA_VANTAGE_API_KEY")


class StockDataFetcher:
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, symbol):
        """
        Initialize with the stock symbol to fetch data for.
        :param symbol: The ticker symbol of the stock (e.g., AAPL).
        """
        self.symbol = symbol

    def get_intraday_data(self, interval="5min"):
        """
        Fetch intraday stock prices.
        :param interval: Interval for the data (e.g., '1min', '5min', '15min').
        :return: JSON response with intraday stock data.
        """
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": self.symbol,
            "interval": interval,
            "apikey": ALPHA_VANTAGE_API_KEY,
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for failed requests
        return response.json()

    def get_historical_data(self):
        """
        Fetch daily historical stock prices.
        :return: JSON response with daily stock data.
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": self.symbol,
            "apikey": ALPHA_VANTAGE_API_KEY,
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
