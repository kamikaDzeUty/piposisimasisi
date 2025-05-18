# tests/adapters/test_tbank_asset_repo.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.adapters.repositories.tbank_asset_repo import TBankAssetRepository
from src.domain.entities.bond import Bond

class DummyClient:
    def list_assets(self, t):
        return [{
            "symbol": "BND1",
            "name": "Bond One",
            "coupon_rate": 5.0,
            "maturity_date": "2030-01-01",
        }]

    def get_price_history(self, sym, per):
        return [100.0, 101.0]


def test_bond_mapping_and_prices():
    repo = TBankAssetRepository(DummyClient())
    assets = repo.list_assets("bond")
    assert len(assets) == 1
    bond = assets[0]
    assert isinstance(bond, Bond)
    assert bond.coupon_rate == 5.0
    assert bond.maturity_date == "2030-01-01"
    assert repo.fetch_prices("BND1", 2) == [100.0, 101.0]
