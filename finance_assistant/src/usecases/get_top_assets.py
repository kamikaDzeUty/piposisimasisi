# src/usecases/get_top_assets.py
from typing import List, Tuple
from src.domain.repositories.asset_repository import AssetRepository
from src.usecases.calculate_sma import calculate_sma
from src.usecases.calculate_ema import calculate_ema

class GetTopAssetsUseCase:
    def __init__(self, repository: AssetRepository, sma_window: int = 14, ema_window: int = 14):
        self.repository = repository
        self.sma_window = sma_window
        self.ema_window = ema_window

    def execute(self, asset_type: str, period: int) -> List[Tuple]:
        assets = self.repository.list_assets(asset_type)
        scored: List[Tuple] = []
        for asset in assets:
            prices = self.repository.fetch_prices(asset.symbol, period)
            if not prices:
                continue
            last_price = prices[-1]
            try:
                sma = calculate_sma(prices, self.sma_window)
                ema = calculate_ema(prices, self.ema_window)
            except ValueError:
                continue
            profitability = last_price - sma
            scored.append((asset, last_price, sma, ema, profitability))
        scored.sort(key=lambda x: x[4], reverse=True)
        return scored[:5]