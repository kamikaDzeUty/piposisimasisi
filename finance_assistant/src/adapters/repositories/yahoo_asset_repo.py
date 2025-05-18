# src/adapters/repositories/yahoo_asset_repo.py

from typing import List
import yfinance as yf
import pandas as pd

from src.domain.repositories.asset_repository import AssetRepository
from src.domain.entities.stock import Stock
from src.domain.entities.currency import Currency
from src.domain.entities.bond import Bond
from src.config.tickers import STOCK_TICKERS, CURRENCY_TICKERS, BOND_TICKERS


class YahooAssetRepository(AssetRepository):
    """
    Берёт тикеры из конфигурации и скачивает их историю через yfinance.
    """

    def list_assets(self, asset_type: str) -> List:
        if asset_type == "stock":
            return [Stock(sym, sym) for sym in STOCK_TICKERS]
        if asset_type == "currency":
            return [Currency(sym, sym) for sym in CURRENCY_TICKERS]
        if asset_type == "bond":
            return [
                Bond(ticker, ticker, coupon_rate=0.0, maturity_date="")
                for ticker in BOND_TICKERS
            ]
        return []

    def fetch_prices(self, symbol: str, period: int) -> List[float]:
        # period — число дней, yfinance принимает строку вида "60d"
        data = yf.download(
            tickers=symbol,
            period=f"{period}d",
            interval="1d",
            progress=False,
            threads=False
        )
        series = data["Close"]
        if isinstance(series, pd.DataFrame):
            series = series.iloc[:, 0]
        return series.dropna().tolist()
