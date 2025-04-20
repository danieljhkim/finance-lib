from .base import BaseInterface
from vibequant.sources.yfinance_source import YFinanceSource

class StockInterface(BaseInterface):
    def __init__(self):
        self.source = YFinanceSource()

    def list_tickers(self):
        return self.source.list_tickers()

    def analyze(self, ticker, start=None, end=None):
        df = self.source.fetch(ticker, start, end)
        return {
        }