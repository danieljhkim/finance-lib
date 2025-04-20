from abc import ABC, abstractmethod

class BaseInterface(ABC):
    
    @abstractmethod
    def list_tickers(self):
        pass

    @abstractmethod
    def fetch(self, ticker: str, start=None, end=None):
        pass