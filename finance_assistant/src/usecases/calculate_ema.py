# src/usecases/calculate_ema.py
from typing import List

def calculate_ema(prices: List[float], window: int) -> float:
    if len(prices) < window:
        raise ValueError(f"Недостаточно данных для расчёта EMA: требуются {window}, а получено {len(prices)}")
    initial_sma = sum(prices[:window]) / window
    alpha = 2 / (window + 1)
    ema = initial_sma
    for price in prices[window:]:
        ema = (price - ema) * alpha + ema
    return ema