from typing import List, Tuple
from src.usecases.calculate_sma import calculate_sma
from src.usecases.calculate_ema import calculate_ema
from src.domain.repositories.asset_repository import AssetRepository

class GetTopAssetsUseCase:
    def __init__(
        self,
        repository: AssetRepository,
        sma_window: int,
        ema_window: int,
    ):
        self.repository = repository
        self.sma_window = sma_window
        self.ema_window = ema_window

    def execute(
        self,
        asset_type: str,
        period: int,
        top_n: int = 5
    ) -> List[Tuple]:
        """
        Возвращает список кортежей:
          (asset, last_price, sma, ema, profit_sma_pct, profit_ema_pct)
        Отсортирован по profit_sma_pct (desc) и обрезан до top_n.
        """
        assets = self.repository.list_assets(asset_type)
        results = []

        for a in assets:
            prices = self.repository.fetch_prices(a.symbol, period)
            if len(prices) < max(self.sma_window, self.ema_window):
                continue

            last = prices[-1]
            sma  = calculate_sma(prices, self.sma_window)
            ema  = calculate_ema(prices, self.ema_window)

            profit_sma_pct = (last - sma) / sma * 100
            profit_ema_pct = (last - ema) / ema * 100

            results.append((a, last, sma, ema, profit_sma_pct, profit_ema_pct))

        # сортируем по абсолютному профиту от SMA
        results.sort(key=lambda x: x[4], reverse=True)
        return results[:top_n]
