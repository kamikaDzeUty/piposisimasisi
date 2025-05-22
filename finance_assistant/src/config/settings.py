# src/config/settings.py

import os
from pathlib import Path
import yaml
from pydantic import BaseModel
from typing import Dict, List

class TickersConfig(BaseModel):
    stock: List[str]
    currency: List[str]
    bond: List[str]

class SchedulerConfig(BaseModel):
    intervals: Dict[str, int]

class RawSettings(BaseModel):
    tickers: TickersConfig
    scheduler: SchedulerConfig
    settings: Dict[str, int]

    @property
    def period(self) -> int:
        return self.settings["period"]

    @property
    def sma_window(self) -> int:
        return self.settings["sma_window"]

    @property
    def ema_window(self) -> int:
        return self.settings["ema_window"]

def load_settings(path: str = None) -> RawSettings:
    # 1) если передан явный путь — используем его
    if path:
        config_path = Path(path)
    else:
        # 2) если в ENV задан CONFIG_FILE — используем его
        env = os.getenv("CONFIG_FILE")
        if env:
            config_path = Path(env)
        else:
            # 3) по умолчанию — файл config.yaml два уровня выше (корень проекта)
            here = Path(__file__).parent        # src/config
            project_root = here.parent.parent    # src/config -> src -> <root>
            config_path = project_root / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return RawSettings(**data)

# глобальный объект
settings = load_settings()
