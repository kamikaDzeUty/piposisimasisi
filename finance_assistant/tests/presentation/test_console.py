# tests/presentation/test_console.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pytest import MonkeyPatch
from io import StringIO
import pytest

# чтобы импортировать run_console
from src.presentation.console import run_console


def test_console_no_data(monkeypatch: MonkeyPatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "2")

    # подменяем класс клиента и репозитория
    monkeypatch.setattr("src.presentation.console.TBankClient", lambda: None)
    class FakeRepo:
        def __init__(self, _): pass
        def list_assets(self, _): return []
        def fetch_prices(self, *_): return []
    monkeypatch.setattr("src.presentation.console.TBankAssetRepository", FakeRepo)

    run_console()
    out = capsys.readouterr().out
    assert "Выберите тип актива" in out
    assert "Нет данных" in out