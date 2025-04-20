from functools import lru_cache
import yfinance as yf
from .base import DataSource
import pandas as pd
from typing import List, Optional
from vibequant.data_loader import load_tickers

_CACHE_SIZE = 128


class YFinanceSource(DataSource):
    """
    Data source for fetching stock and crypto data using yfinance.
    """

    def __init__(self):
        super().__init__()
        tickers = load_tickers()
        self.stock_tickers: List[str] = tickers.get("sp500", [])
        self.crypto_tickers: List[str] = tickers.get("crypto_yahoo", [])

    def list_stock_tickers(self) -> List[str]:
        """
        Returns a list (none exhaustive) of supported stock tickers.
        """
        return self.stock_tickers

    def list_crypto_tickers(self) -> List[str]:
        """
        Returns a list (none exhaustive) of supported crypto tickers.
        """
        return self.crypto_tickers

    @lru_cache(maxsize=_CACHE_SIZE)
    def fetch(
        self, ticker: str, start: Optional[str] = None, end: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetches historical data for a given ticker between start and end dates.

        Args:
            ticker (str): The ticker symbol to fetch data for.
            start (Optional[str]): The start date (YYYY-MM-DD).
            end (Optional[str]): The end date (YYYY-MM-DD).

        Returns:
            pd.DataFrame: DataFrame with historical data and additional columns.
        """
        if not isinstance(ticker, str) or not ticker:
            raise ValueError("Ticker must be a non-empty string.")

        df = yf.download(ticker, start=start, end=end)
        if df.empty:
            return pd.DataFrame()  # Return empty DataFrame if no data

        df = df.copy()
        df["Change"] = ((df["Close"] - df["Open"]) / df["Open"]) * 100
        df["DayOfMonth"] = df.index.day
        df["Weekday"] = df.index.day_name()
        return df
