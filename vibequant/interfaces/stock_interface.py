from .base import BaseInterface
from vibequant.sources.yfinance_source import YFinanceSource
from vibequant.wrappers.vibes import VibeFrame

class StockInterface(BaseInterface):
    
    def __init__(self):
        self.sources = {
            'yfinance': YFinanceSource()
        }
        
    def list_tickers(self, source='yfinance'):
        return self._get_source(source).list_stock_tickers()
