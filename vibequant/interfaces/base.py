from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from vibequant.sources.yfinance_source import YFinanceSource
from vibequant.wrappers.vibes import VibeFrame


class BaseInterface(ABC):
    """
    Abstract base class for financial data interfaces.
    Provides methods to fetch and analyze stock data from various sources.
    """

    WEEK_DAYS: List[str] = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    def __init__(self) -> None:
        """
        Initialize the BaseInterface with available data sources.
        """
        self.sources: Dict[str, Any] = {"yfinance": YFinanceSource()}

    def list_sources(self) -> List[str]:
        """
        List all available data sources.

        Returns:
            List[str]: Names of available sources.
        """
        return list(self.sources.keys())

    def _get_source(self, source: str) -> Any:
        """
        Retrieve a data source by name.

        Args:
            source (str): The name of the data source.

        Returns:
            Any: The data source object.

        Raises:
            ValueError: If the source is not found.
        """
        if source not in self.sources:
            raise ValueError(
                f"Source '{source}' not found. Available sources: {', '.join(self.sources.keys())}"
            )
        return self.sources[source]

    def list_tickers(self, source: str = "yfinance") -> List[str]:
        """
        List available stock tickers from a data source.

        Args:
            source (str): The name of the data source.

        Returns:
            List[str]: List of ticker symbols.
        """
        return self._get_source(source).list_stock_tickers()

    def avg_by_weekday(
        self, ticker: str, start: Optional[str] = None, end: Optional[str] = None, source: str = "yfinance"
    ) -> VibeFrame:
        """
        Calculate average change by weekday for a given ticker.

        Args:
            ticker (str): The ticker symbol.
            start (str, optional): Start date.
            end (str, optional): End date.
            source (str): Data source name.

        Returns:
            VibeFrame: Resulting data wrapped in a VibeFrame.
        """
        df = self._get_source(source).fetch(ticker, start, end)
        wdf = df.groupby("Weekday")["Change"].mean()
        wdf = wdf.reindex(self.WEEK_DAYS)
        wdf_df = wdf.to_frame(name="AvgChange")
        vf = VibeFrame(wdf_df, type="W")
        vf.original_df = df
        return vf

    def avg_by_day_of_month(
        self, ticker: str, start: Optional[str] = None, end: Optional[str] = None, source: str = "yfinance"
    ) -> VibeFrame:
        """
        Calculate average change by day of month for a given ticker.

        Args:
            ticker (str): The ticker symbol.
            start (str, optional): Start date.
            end (str, optional): End date.
            source (str): Data source name.

        Returns:
            VibeFrame: Resulting data wrapped in a VibeFrame.
        """
        df = self._get_source(source).fetch(ticker, start, end)
        dom_df = df.groupby("DayOfMonth")["Change"].mean()
        dom_df = dom_df.reindex(range(1, 32))
        dom_df = dom_df.to_frame(name="AvgChange")
        vf = VibeFrame(dom_df, type="M")
        vf.original_df = df
        return vf

    def avg_by_weekday_and_dom(
        self, ticker: str, start: Optional[str] = None, end: Optional[str] = None, source: str = "yfinance"
    ) -> VibeFrame:
        """
        Calculate average change by both weekday and day of month for a given ticker.

        Args:
            ticker (str): The ticker symbol.
            start (str, optional): Start date.
            end (str, optional): End date.
            source (str): Data source name.

        Returns:
            VibeFrame: Resulting data wrapped in a VibeFrame.
        """
        df = self._get_source(source).fetch(ticker, start, end)
        pivot = (
            df.groupby(["DayOfMonth", "Weekday"])["Change"]
            .mean()
            .unstack(fill_value=0)
        )
        pivot = pivot.reindex(columns=self.WEEK_DAYS, fill_value=0)
        pivot.index.name = "DayOfMonth"
        vf = VibeFrame(pivot, type="WM")
        vf.original_df = df
        return vf