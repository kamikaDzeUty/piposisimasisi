# src/domain/entities/stock.py
from .asset import Asset
from typing import List

class Stock(Asset):
    """
    Акция эмитента.
    """
    def __init__(self, symbol: str, name: str):
        super().__init__(symbol, name)

    def get_price_history(self, period: int) -> List[float]:
        raise NotImplementedError