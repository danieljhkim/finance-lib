from .interfaces.stock_interface import StockInterface
from .interfaces.crypto_interface import CryptoInterface
from .wrappers.vibes import VibeFrame

vstock = StockInterface()
vcrypto = CryptoInterface()

__author__ = "danieljhkim"
__version__ = "0.1.0"
__all__ = ["vstock", "vcrypto", "VibeFrame"]

