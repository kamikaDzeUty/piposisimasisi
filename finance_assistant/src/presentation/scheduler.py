# src/presentation/scheduler.py

from datetime import datetime, timedelta
from typing import Dict, Tuple

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.adapters.repositories.yahoo_asset_repo import YahooAssetRepository
from src.usecases.get_top_assets import GetTopAssetsUseCase
from src.presentation.utils import format_table
from src.config.settings import settings


class AssetScheduler:
    """
    Планировщик периодических задач по типам активов:
      - акции — каждая stock_interval минуты,
      - валюта — каждая currency_interval минуты,
      - облигации — каждая bond_interval минуты.
    Корректно обрабатывает команды и завершает работу по 'выход'.
    """
    def __init__(self):
        self.repo = YahooAssetRepository()
        self.usecase = GetTopAssetsUseCase(
            self.repo,
            sma_window=settings.sma_window,
            ema_window=settings.ema_window
        )
        self.jobs_config: Dict[str, Tuple[str, int]] = {
            "акции":     ("stock",    settings.scheduler.intervals["stock"]),
            "валюта":    ("currency", settings.scheduler.intervals["currency"]),
            "облигации": ("bond",     settings.scheduler.intervals["bond"]),
        }
        self.scheduler = BackgroundScheduler()

    def _run_job(self, asset_type: str, label: str):
        data = self.usecase.execute(asset_type, period=settings.period)
        print(f"\n[{datetime.now():%H:%M:%S}] {label}:")
        headers = [
            "Symbol", "Name", "Last Price",
            f"SMA({self.usecase.sma_window})",
            f"EMA({self.usecase.ema_window})",
            "Profit"
        ]
        rows = [
            [
                a.symbol,
                a.name,
                f"{last:.4f}",
                f"{sma:.4f}",
                f"{ema:.4f}",
                f"{prof:.4f}"
            ]
            for a, last, sma, ema, prof in data
        ]
        print(format_table(headers, rows))

    def schedule_jobs(self):
        for cmd, (asset_type, minutes) in self.jobs_config.items():
            self.scheduler.add_job(
                func=lambda at=asset_type, lbl=cmd: self._run_job(at, lbl.capitalize()),
                trigger=IntervalTrigger(minutes=minutes),
                id=cmd
            )

    def start(self):
        self.schedule_jobs()
        self.scheduler.start()

        print("Периодические задачи запущены.")
        print("Доступные команды: акции, валюта, облигации, выход")

        try:
            while True:
                cmd = input(">>> ").strip().lower()
                if cmd == "выход":
                    print("Завершение по команде пользователя…")
                    break

                if cmd in self.jobs_config:
                    asset_type, interval = self.jobs_config[cmd]
                    # Немедленный запуск и сброс таймера
                    self._run_job(asset_type, cmd.capitalize())
                    next_time = datetime.now() + timedelta(minutes=interval)
                    self.scheduler.modify_job(job_id=cmd, next_run_time=next_time)
                else:
                    print("Неизвестная команда. Попробуйте ещё раз.")
        except (KeyboardInterrupt, EOFError):
            print("\nПолучен прерывающий сигнал, завершение…")
        finally:
            self.scheduler.shutdown()
            # Метод просто возвращается — код после start_scheduler() может выполниться

def start_scheduler():
    AssetScheduler().start()
