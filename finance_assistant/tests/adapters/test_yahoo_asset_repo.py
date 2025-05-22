import pandas as pd
import pytest
from unittest.mock import patch

from src.adapters.repositories.yahoo_asset_repo import YahooAssetRepository
from src.config.settings import settings
from src.domain.entities.stock import Stock
from src.domain.entities.currency import Currency
from src.domain.entities.bond import Bond


def test_list_assets_returns_correct_types_and_counts():
    # Сток-активы
    stocks = YahooAssetRepository.list_assets("stock")
    assert isinstance(stocks, list)
    assert len(stocks) == len(settings.tickers.stock)
    assert all(isinstance(a, Stock) for a in stocks)
    # Валюты
    currs = YahooAssetRepository.list_assets("currency")
    assert len(currs) == len(settings.tickers.currency)
    assert all(isinstance(a, Currency) for a in currs)
    # Облигации
    bonds = YahooAssetRepository.list_assets("bond")
    assert len(bonds) == len(settings.tickers.bond)
    assert all(isinstance(a, Bond) for a in bonds)
    # Неизвестный тип — пустой список
    assert YahooAssetRepository.list_assets("foo") == []


@patch("yfinance.download")
def test_fetch_prices_simple_series(mock_download):
    # yfinance возвращает DataFrame с одним столбцом Close
    df = pd.DataFrame({"Close": [1.0, 2.0, 3.0]})
    mock_download.return_value = df
    prices = YahooAssetRepository.fetch_prices("SYM", period=5)
    assert prices == [1.0, 2.0, 3.0]


@patch("yfinance.download")
def test_fetch_prices_multiindex_columns(mock_download):
    # Эмулируем DataFrame с MultiIndex-столбцами, где Close → несколько тикеров
    df = pd.DataFrame({
        ("Close", "TK1"): [10, 20],
        ("Close", "TK2"): [30, None]
    })
    df.columns = pd.MultiIndex.from_tuples(df.columns)
    mock_download.return_value = df
    prices = YahooAssetRepository.fetch_prices("TK1", period=7)
    # Должен выбрать первый столбец (Close, TK1) и отбросить None
    assert prices == [10, 20]
