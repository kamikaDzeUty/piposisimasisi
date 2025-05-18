import sys
from typing import List, Tuple

from src.adapters.repositories.yahoo_asset_repo import YahooAssetRepository
from src.usecases.get_top_assets import GetTopAssetsUseCase


def run_console():
    print("Выберите тип актива:")
    print("1 — облигации")
    print("2 — акции")
    print("3 — валюта")
    choice = input("Ваш выбор [1-3]: ").strip()
    mapping = {"1": "bond", "2": "stock", "3": "currency"}
    asset_type = mapping.get(choice)
    if not asset_type:
        print("Неверный выбор. Выход.")
        sys.exit(1)

    # жёстко фиксируем период и окна
    period = 60
    sma_window = 14
    ema_window = 14

    # вместо TBankClient + TBankAssetRepository
    repo = YahooAssetRepository()
    uc = GetTopAssetsUseCase(repo, sma_window=sma_window, ema_window=ema_window)

    res = uc.execute(asset_type, period)
    if not res:
        print("Нет данных для выбранного типа актива или недостаточно исторических данных.")
        return

    headers = ["Symbol", "Name", "Last Price", f"SMA({sma_window})", f"EMA({ema_window})", "Profit"]
    rows: List[Tuple] = []
    for a, last, sma, ema, prof in res:
        rows.append([
            a.symbol, a.name,
            f"{last:.4f}", f"{sma:.4f}", f"{ema:.4f}", f"{prof:.4f}"
        ])

    # вычисляем ширины колонок
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    # печатаем заголовок
    hdr = " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers)))
    sep = "-+-".join("-" * widths[i] for i in range(len(headers)))
    print(hdr)
    print(sep)
    for row in rows:
        print(" | ".join(row[i].ljust(widths[i]) for i in range(len(headers))))
