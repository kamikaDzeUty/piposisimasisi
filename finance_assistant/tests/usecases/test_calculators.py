import pytest
from ...src.usecases.calculate_sma import calculate_sma
from ...src.usecases.calculate_ema import calculate_ema

def test_calculate_sma_basic():
    assert calculate_sma([1, 2, 3, 4, 5], window=3) == pytest.approx(4.0)

def test_calculate_sma_insufficient():
    with pytest.raises(ValueError):
        calculate_sma([1, 2], window=3)

def test_calculate_ema_basic():
    prices = [10, 20, 30, 40]
    # initial EMA должен получиться 35
    assert calculate_ema(prices, window=2) == pytest.approx(35.0)
