# src/domain/repositories/asset_repository.py
from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.asset import Asset

class AssetRepository(ABC):
    """
    Интерфейс репозитория для получения списка активов и их исторических цен.
    """
    @abstractmethod
    def list_assets(self, asset_type: str) -> List[Asset]:
        """
        Возвращает список объектов Asset заданного типа.
        """
        raise NotImplementedError

    @abstractmethod
    def fetch_prices(self, symbol: str, period: int) -> List[float]:
        """
        Возвращает список исторических цен для актива.
        """
        raise NotImplementedError