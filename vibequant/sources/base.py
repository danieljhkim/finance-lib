from abc import ABC, abstractmethod

class DataSource(ABC):
    
    @abstractmethod
    def list_tickers(self):
        pass

    @abstractmethod
    def fetch(self, ticker: str, start=None, end=None):
        pass