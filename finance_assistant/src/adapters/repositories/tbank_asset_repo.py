# src/adapters/repositories/tbank_asset_repo.py
from typing import List
from src.domain.repositories.asset_repository import AssetRepository
from src.domain.entities.bond import Bond
from src.domain.entities.stock import Stock
from src.domain.entities.currency import Currency
from src.infrastructure.tbank_client import TBankClient

class TBankAssetRepository(AssetRepository):
    """
    Реализация AssetRepository через API Т-Банка.
    """
    def __init__(self, client: TBankClient):
        self.client = client

    def list_assets(self, asset_type: str) -> List:
        raw_assets = self.client.list_assets(asset_type)
        entities: List = []
        for item in raw_assets:
            symbol = item.get('symbol')
            name = item.get('name')
            if asset_type == 'bond':
                coupon_rate = item.get('coupon_rate', 0.0)
                maturity_date = item.get('maturity_date', '')
                entities.append(Bond(symbol, name, coupon_rate, maturity_date))
            elif asset_type == 'stock':
                entities.append(Stock(symbol, name))
            elif asset_type == 'currency':
                entities.append(Currency(symbol, name))
        return entities

    def fetch_prices(self, symbol: str, period: int) -> List[float]:
        return self.client.get_price_history(symbol, period)
