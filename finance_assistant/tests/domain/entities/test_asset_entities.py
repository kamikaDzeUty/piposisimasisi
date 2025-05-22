import pytest
from src.domain.entities.asset import Asset
from src.domain.entities.bond import Bond
from src.domain.entities.stock import Stock
from src.domain.entities.currency import Currency

def test_asset_is_abstract():
    with pytest.raises(TypeError):
        Asset("SYM", "Name")

def test_bond_attributes_and_get_price_history():
    b = Bond("BND1", "Bond One", coupon_rate=5.0, maturity_date="2030-01-01")
    assert isinstance(b, Asset)
    assert b.symbol == "BND1"
    assert b.name == "Bond One"
    assert b.coupon_rate == 5.0
    assert b.maturity_date == "2030-01-01"
    with pytest.raises(NotImplementedError):
        b.get_price_history(10)

def test_stock_attributes_and_get_price_history():
    s = Stock("STK", "Stock One")
    assert isinstance(s, Asset)
    assert s.symbol == "STK"
    assert s.name == "Stock One"
    with pytest.raises(NotImplementedError):
        s.get_price_history(5)

def test_currency_attributes_and_get_price_history():
    c = Currency("CUR", "Currency One")
    assert isinstance(c, Asset)
    assert c.symbol == "CUR"
    assert c.name == "Currency One"
    with pytest.raises(NotImplementedError):
        c.get_price_history(1)
