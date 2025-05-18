# src/presentation/console.py
import sys
from typing import List, Tuple
from src.infrastructure.tbank_client import TBankClient
from src.adapters.repositories.tbank_asset_repo import TBankAssetRepository
from src.usecases.get_top_assets import GetTopAssetsUseCase

def run_console():
    print("Выберите тип актива:")
    print("1 — облигации")
    print("2 — акции")
    print("3 — валюта")
    choice = input("Ваш выбор [1-3]: ").strip()

    mapping = {"1": "bond", "2": "stock", "3": "currency"}
    asset_type = mapping.get(choice)
    if asset_type is None:
        print("Неверный выбор. Выход.")
        sys.exit(1)

    period = 60
    sma_window = 14
    ema_window = 14

    try:
        client = TBankClient()
        repository = TBankAssetRepository(client)
        use_case = GetTopAssetsUseCase(repository, sma_window=sma_window, ema_window=ema_window)
    except Exception as e:
        print(f"Ошибка инициализации: {e}")
        sys.exit(1)

    try:
        results: List[Tuple] = use_case.execute(asset_type, period)
    except Exception as e:
        print(f"Ошибка при выполнении расчётов: {e}")
        sys.exit(1)

    if not results:
        print("Нет данных для выбранного типа актива или недостаточно исторических данных.")
        return

    headers = ["Symbol", "Name", "Last Price", f"SMA({sma_window})", f"EMA({ema_window})", "Profitability"]
    rows = []
    for asset, last_price, sma, ema, profit in results:
        rows.append([
            asset.symbol,
            asset.name,
            f"{last_price:.4f}",
            f"{sma:.4f}",
            f"{ema:.4f}",
            f"{profit:.4f}"
        ])

    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    separator = "-+-".join('-' * col_widths[i] for i in range(len(headers)))
    print(header_line)
    print(separator)
    for row in rows:
        print(" | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(row)))

if __name__ == '__main__':
    run_console()