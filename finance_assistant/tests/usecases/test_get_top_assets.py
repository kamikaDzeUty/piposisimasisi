import pytest
from src.usecases.get_top_assets import GetTopAssetsUseCase
from src.domain.entities.stock import Stock

class DummyRepo:
    def list_assets(self, asset_type):
        return [
            Stock("AAA", "A Corp"),
            Stock("BBB", "B Corp"),
            Stock("CCC", "C Corp")
        ]
    def fetch_prices(self, symbol, period):
        # AAA: rising, BBB: falling, CCC: flat
        if symbol == "AAA":
            return [1, 2, 3, 4]
        if symbol == "BBB":
            return [4, 3, 2, 1]
        return [5, 5, 5, 5]

def test_get_top_assets_order_and_limit():
    uc = GetTopAssetsUseCase(DummyRepo(), sma_window=2, ema_window=2)
    top = uc.execute("stock", period=4)
    # profitability: AAA:4-3=1, BBB:1-1.5=-0.5, CCC:5-5=0 → order AAA, CCC, BBB
    symbols = [asset.symbol for asset, *_ in top]
    assert symbols == ["AAA", "CCC", "BBB"]
    # если больше 5 активов, ограничение топ-5
    # здесь всего 3, значит len=3
    assert len(top) == 3

def test_get_top_assets_skips_insufficient_history():
    class ShortRepo(DummyRepo):
        def list_assets(self, asset_type):
            return [Stock("X", "X Corp")]
        def fetch_prices(self, symbol, period):
            return [1]  # меньше sma_window=3
    uc = GetTopAssetsUseCase(ShortRepo(), sma_window=3, ema_window=3)
    assert uc.execute("stock", period=1) == []
