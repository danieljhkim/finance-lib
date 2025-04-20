from typing import List
from .base import BaseInterface
from vibequant.sources.coingecko_source import CoinGeckoSource
from vibequant.sources.yfinance_source import YFinanceSource

class CryptoInterface(BaseInterface):
    """
    Interface for cryptocurrency data sources, extending BaseInterface.
    """

    def __init__(self) -> None:
        """
        Initialize the CryptoInterface with available crypto data sources.
        """
        super().__init__()
        # You can uncomment or add more sources as needed
        self.sources = {
            # "coingecko": CoinGeckoSource(),
            "yfinance": YFinanceSource()
        }

    def list_tickers(self, source: str = "yfinance") -> List[str]:
        """
        List available cryptocurrency tickers from a data source.

        Args:
            source (str): The name of the data source.

        Returns:
            List[str]: List of cryptocurrency ticker symbols.
        """
        return self._get_source(source).list_crypto_tickers()