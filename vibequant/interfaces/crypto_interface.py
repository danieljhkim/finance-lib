from .base import BaseInterface
from vibequant.sources.coingecko_source import CoinGeckoSource
from vibequant.sources.yfinance_source import YFinanceSource

class CryptoInterface(BaseInterface):
    
    def __init__(self):
        self.sources = {
            'coingecko': CoinGeckoSource(),
            'yfinance': YFinanceSource()
        }

    def list_sources(self):
        return list(self.sources.keys())
    
    def list_tickers(self, source='yfinance'):
        return self._get_source(source).list_crypto_tickers()
