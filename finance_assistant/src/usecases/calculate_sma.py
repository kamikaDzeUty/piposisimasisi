# src/usecases/calculate_sma.py
from typing import List

def calculate_sma(prices: List[float], window: int) -> float:
    if len(prices) < window:
        raise ValueError(f"Недостаточно данных для расчёта SMA: требуются {window}, а получено {len(prices)}")
    return sum(prices[-window:]) / window
