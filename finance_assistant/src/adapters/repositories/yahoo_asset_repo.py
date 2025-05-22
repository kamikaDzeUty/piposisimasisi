# src/adapters/repositories/yahoo_asset_repo.py

from typing import List
import yfinance as yf
import pandas as pd

from src.domain.repositories.asset_repository import AssetRepository
from src.domain.entities.stock import Stock
from src.domain.entities.currency import Currency
from src.domain.entities.bond import Bond
from src.config.settings import settings


class YahooAssetRepository(AssetRepository):
    """
    Берёт тикеры из конфигурации и скачивает их историю через yfinance.
    """

    @staticmethod
    def list_assets(asset_type: str) -> List:
        if asset_type == "stock":
            return [Stock(s, s) for s in settings.tickers.stock]
        if asset_type == "currency":
            return [Currency(s, s) for s in settings.tickers.currency]
        if asset_type == "bond":
            return [
                Bond(s, s, coupon_rate=0.0, maturity_date="")
                for s in settings.tickers.bond
            ]
        return []

    @staticmethod
    def fetch_prices(symbol: str, period: int) -> List[float]:
        # period передаётся извне, но по умолчанию берём settings.period
        days = f"{period}d"
        data = yf.download(
            tickers=symbol,
            period=days,
            interval="1d",
            progress=False,
            threads=False
        )
        series = data["Close"]
        if isinstance(series, pd.DataFrame):
            series = series.iloc[:, 0]
        return series.dropna().tolist()
