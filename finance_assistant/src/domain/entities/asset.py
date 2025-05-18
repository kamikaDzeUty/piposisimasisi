# src/domain/entities/asset.py
from abc import ABC, abstractmethod
from typing import List

class Asset(ABC):
    """
    Базовый класс для всех типов активов.
    """
    def __init__(self, symbol: str, name: str):
        self.symbol = symbol
        self.name = name

    @abstractmethod
    def get_price_history(self, period: int) -> List[float]:
        """
        Возвращает исторические цены за последние `period` периодов.
        """
        raise NotImplementedError
