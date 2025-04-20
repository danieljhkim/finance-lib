from .base import BaseInterface
from vibequant.sources.coingecko_source import CoinGeckoSource

class CryptoInterface(BaseInterface):
    
    def __init__(self):
        self.source = CoinGeckoSource()

    def list_tickers(self):
        return self.source.list_tickers()

    def analyze(self, ticker, start=None, end=None):
        df = self.source.fetch(ticker, start, end)
        return {
        }