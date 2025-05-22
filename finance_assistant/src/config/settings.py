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
    ticker_names: Dict[str, str] = {}

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
    if path:
        config_path = Path(path)
    else:
        env_path = os.getenv("CONFIG_FILE")
        if env_path:
            config_path = Path(env_path)
        else:
            here = Path(__file__).parent
            project_root = here.parent.parent
            config_path = project_root / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    return RawSettings(**data)

settings = load_settings()
