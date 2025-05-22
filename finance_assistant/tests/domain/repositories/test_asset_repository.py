import pytest
from src.domain.repositories.asset_repository import AssetRepository
from src.domain.entities.stock import Stock

class DummyRepo(AssetRepository):
    def list_assets(self, asset_type: str):
        return [Stock("A","A Corp")]
    def fetch_prices(self, symbol: str, period: int):
        return [1.23, 4.56]

def test_cannot_instantiate_asset_repository_directly():
    with pytest.raises(TypeError):
        AssetRepository()

def test_dummy_repo_implements_asset_repository():
    repo = DummyRepo()
    assets = repo.list_assets("stock")
    assert len(assets) == 1
    assert isinstance(assets[0], Stock)
    prices = repo.fetch_prices("A", 2)
    assert prices == [1.23, 4.56]
