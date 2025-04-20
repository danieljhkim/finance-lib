from .interfaces.stock_interface import StockInterface
from .interfaces.crypto_interface import CryptoInterface

stock = StockInterface()
crypto = CryptoInterface()

__author__ = "danieljhkim"
__version__ = "0.1.0"
__all__ = ["stock", "crypto"]
