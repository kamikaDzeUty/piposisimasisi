# src/domain/entities/bond.py
from .asset import Asset
from typing import List

class Bond(Asset):
    """
    Облигация с купонной доходностью и датой погашения.
    """
    def __init__(self, symbol: str, name: str, coupon_rate: float, maturity_date: str):
        super().__init__(symbol, name)
        self.coupon_rate = coupon_rate
        self.maturity_date = maturity_date

    def get_price_history(self, period: int) -> List[float]:
        raise NotImplementedError