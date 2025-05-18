# src/domain/entities/currency.py
from .asset import Asset
from typing import List

class Currency(Asset):
    """
    Валютная пара или валюта.
    """
    def __init__(self, symbol: str, name: str):
        super().__init__(symbol, name)

    def get_price_history(self, period: int) -> List[float]:
        raise NotImplementedError