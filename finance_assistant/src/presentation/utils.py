# src/presentation/utils.py

from typing import List

def format_table(
    headers: List[str],
    rows: List[List[str]]
) -> str:
    """
    Считает оптимальные ширины колонок по заголовкам и ячейкам,
    собирает и возвращает одну большую строку таблицы.
    """
    # 1) вычисляем ширины
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    # 2) строим строки
    hdr = " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers)))
    sep = "-+-".join("-" * widths[i] for i in range(len(headers)))
    lines = [hdr, sep]
    for row in rows:
        line = " | ".join(row[i].ljust(widths[i]) for i in range(len(headers)))
        lines.append(line)

    return "\n".join(lines)
