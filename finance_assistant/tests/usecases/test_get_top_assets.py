# tests/usecases/test_get_top_assets.py
import sys
import os
# Вставляем проектную папку, чтобы Python нашёл пакет src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.usecases.get_top_assets import GetTopAssetsUseCase
from src.domain.entities.stock import Stock

class DummyRepo:
    def list_assets(self, _):
        return [Stock("AAA", "A Corp"), Stock("BBB", "B Corp")]

    def fetch_prices(self, symbol, _):
        return [1, 2, 3, 4] if symbol == "AAA" else [4, 3, 2, 1]


def test_get_top_assets_ordering():
    uc = GetTopAssetsUseCase(DummyRepo(), sma_window=2, ema_window=2)
    result = uc.execute("stock", period=4)
    symbols = [asset.symbol for asset, *_ in result]
    assert symbols == ["AAA", "BBB"]