import os
import yaml
import pytest
from pathlib import Path

from src.config.settings import load_settings, RawSettings


def make_config_dict():
    return {
        "tickers": {
            "stock": ["AAA", "BBB"],
            "currency": ["EURUSD=X", "GBPUSD=X"],
            "bond": ["^TNX"]
        },
        "scheduler": {
            "intervals": {"stock": 5, "currency": 10, "bond": 15}
        },
        "settings": {"period": 30, "sma_window": 7, "ema_window": 8}
    }


def test_load_settings_from_explicit_path(tmp_path):
    cfg_data = make_config_dict()
    cfg_file = tmp_path / "config.yaml"
    cfg_file.write_text(yaml.safe_dump(cfg_data), encoding="utf-8")

    settings = load_settings(str(cfg_file))
    assert isinstance(settings, RawSettings)
    # Проверяем свойства
    assert settings.period == 30
    assert settings.sma_window == 7
    assert settings.ema_window == 8
    # Проверяем tickers
    assert settings.tickers.stock == ["AAA", "BBB"]
    assert settings.tickers.currency == ["EURUSD=X", "GBPUSD=X"]
    assert settings.tickers.bond == ["^TNX"]
    # Проверяем интервалы
    assert settings.scheduler.intervals["stock"] == 5
    assert settings.scheduler.intervals["currency"] == 10
    assert settings.scheduler.intervals["bond"] == 15


def test_load_settings_via_env_var(tmp_path, monkeypatch):
    cfg_data = make_config_dict()
    cfg_file = tmp_path / "env_config.yaml"
    cfg_file.write_text(yaml.safe_dump(cfg_data), encoding="utf-8")

    # Устанавливаем переменную окружения
    monkeypatch.setenv("CONFIG_FILE", str(cfg_file))

    settings = load_settings()
    # Должен загрузиться тот же конфиг
    assert settings.scheduler.intervals["stock"] == 5
    assert settings.period == 30


def test_load_settings_file_not_found(tmp_path):
    missing = tmp_path / "nope.yaml"
    with pytest.raises(FileNotFoundError):
        load_settings(str(missing))
