import pytest
from src.usecases.calculate_sma import calculate_sma
from src.usecases.calculate_ema import calculate_ema

def test_calculate_sma_basic():
    prices = [1, 2, 3, 4, 5]
    assert calculate_sma(prices, window=3) == pytest.approx((3 + 4 + 5) / 3)

def test_calculate_sma_exact_length():
    prices = [10, 20, 30]
    assert calculate_sma(prices, window=3) == pytest.approx(20.0)

def test_calculate_sma_all_same():
    prices = [5.0] * 10
    assert calculate_sma(prices, window=5) == pytest.approx(5.0)

def test_calculate_sma_insufficient_data():
    with pytest.raises(ValueError):
        calculate_sma([1, 2], window=3)

def test_calculate_ema_basic():
    # window=2 ⇒ initial=(10+20)/2=15, α=2/3
    # ema1=(30−15)*2/3+15=25; ema2=(40−25)*2/3+25=35
    result = calculate_ema([10, 20, 30, 40], window=2)
    assert result == pytest.approx(35.0)

def test_calculate_ema_constant_series():
    prices = [7.5] * 8
    assert calculate_ema(prices, window=3) == pytest.approx(7.5)

def test_calculate_ema_window_one():
    prices = [2, 4, 6, 8]
    # window=1 ⇒ α=1 ⇒ ema always equals price ⇒ final = last price = 8
    assert calculate_ema(prices, window=1) == pytest.approx(8.0)

def test_calculate_ema_insufficient_data():
    with pytest.raises(ValueError):
        calculate_ema([1, 2], window=3)
