from abc import ABC, abstractmethod

class DataSource(ABC):
    

    @abstractmethod
    def fetch(self, ticker: str, start=None, end=None):
        pass