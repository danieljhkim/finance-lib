from typing import List
from .base import BaseInterface
from vibequant.sources.yfinance_source import YFinanceSource

class StockInterface(BaseInterface):
    """
    Interface for stock data sources, extending BaseInterface.
    """

    WEEK_DAYS: List[str] = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
    ]

    def __init__(self) -> None:
        """
        Initialize the StockInterface with available stock data sources.
        """
        super().__init__()
        # Override sources if needed, or extend
        self.sources = {
            "yfinance": YFinanceSource()
        }

    def list_tickers(self, source: str = "yfinance") -> List[str]:
        """
        List available stock tickers from a data source.

        Args:
            source (str): The name of the data source.

        Returns:
            List[str]: List of ticker symbols.
        """
        return self._get_source(source).list_stock_tickers()