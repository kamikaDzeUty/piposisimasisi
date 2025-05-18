# src/config/tickers.py

"""
Списки тикеров для YahooAssetRepository.
"""

# Топ-20 наиболее ликвидных акций США (по рыночной капитализации)
STOCK_TICKERS = [
    "AAPL",  # Apple
    "MSFT",  # Microsoft
    "GOOG",  # Alphabet Class C
    "AMZN",  # Amazon
    "TSLA",  # Tesla
    "NVDA",  # NVIDIA
    "META",  # Facebook/Meta
    "BRK-B", # Berkshire Hathaway B
    "JPM",   # JPMorgan Chase
    "UNH",   # UnitedHealth Group
    "V",     # Visa
    "PG",    # Procter & Gamble
    "JNJ",   # Johnson & Johnson
    "HD",    # Home Depot
    "MA",    # Mastercard
    "BAC",   # Bank of America
    "XOM",   # Exxon Mobil
    "PFE",   # Pfizer
    "KO",    # Coca-Cola
    "TM"     # Toyota Motor
]

# Популярные валютные пары
CURRENCY_TICKERS = [
    "EURUSD=X",  # евро/доллар США
    "GBPUSD=X",  # фунт стерлингов/доллар США
    "USDJPY=X",  # доллар США/иена
    "USDCAD=X",  # доллар США/канадский доллар
    "AUDUSD=X",  # австралийский доллар/доллар США
    "USDCHF=X",  # доллар США/швейцарский франк
    "NZDUSD=X",  # новозеландский доллар/доллар США
    "EURGBP=X",  # евро/фунт стерлингов
    "EURJPY=X",  # евро/иена
    "EURAUD=X"   # евро/австрал. доллар
]

# Тикеры доходностей государственных облигаций США на Yahoo Finance
BOND_TICKERS = [
    "^IRX",   # 13-недельные T-Bill
    "^FVX",   # 5-летние T-Note
    "^TNX",   # 10-летние T-Note
    "^TYX"    # 30-летние T-Bond
]
