from .base import DataSource

class CoinGeckoSource(DataSource):
    def list_tickers(self):
        # Placeholder or custom logic
        return []

    def fetch(self, ticker, start=None, end=None):
        return []