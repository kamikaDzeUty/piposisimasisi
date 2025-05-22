finance_assistant/  
├── config.yaml               # YAML-конфигурация: тикеры, интервалы, period, sma/ema окна  
├── requirements.txt          # зависимости проекта
│  
├── src/
│   ├── config
│   │   └── settings.py       # загрузка config.yaml в объект settings  
│   │  
│   ├── domain/               # бизнес-логика
│   │   ├── entities/         # доменные сущности  
│   │   │   ├── asset.py      # абстрактный класс Asset
│   │   │   ├── bond.py       # сущность Bond (облигация)  
│   │   │   ├── stock.py      # сущность Stock (акция)  
│   │   │   ├── currency.py   # сущность Currency (валюта)  
│   │   │   └── user.py       # сущность User (пользователь)  
│   │   └── repositories/
│   │       ├── asset_repository.py  # интерфейс для получения цен активов  
│   │       └── user_repository.py   # интерфейс для хранения/поиска пользователей  
│   │  
│   ├── usecases/             # сценарии 
│   │   ├── calculate_sma.py  # расчёт простого скользящего среднего  
│   │   ├── calculate_ema.py  # расчёт экспоненциального скользящего среднего  
│   │   ├── get_top_assets.py # логика «топ-5 активов»  
│   │   └── register_user.py  # сценарий регистрации пользователя  
│   │  
│   ├── adapters/             # реализации контрактов (внешние сервисы)  
│   │   └── repositories/
│   │       ├── yahoo_asset_repo.py       # AssetRepository через yfinance  
│   │       └── inmemory_user_repository.py # UserRepository в памяти (заглушка)  
│   │  
│   ├── presentation/         # интерфейсы ввода-вывода  
│   │   ├── utils.py          # format_table, реализация таблицы
│   │   ├── scheduler.py      # фоновый планировщик задач (APScheduler)  
│   │   └── auth_console.py   # CLI-заглушка для регистрации пользователя  
│   │  
│   └── main.py               # точка входа: выбор режима (scheduler или регистрация)  
│  
└── tests/                    # тесты pytest  
    ├── conftest.py          # настройка PYTHONPATH для тестов  
    │  
    ├── config/              # тесты конфигурации  
    │   └── test_settings.py # загрузка и валидация config.yaml  
    │  
    ├── domain/              # тесты домена  
    │   ├── entities/        # тесты сущностей  
    │   │   ├── test_asset_entities.py # Asset, Bond, Stock, Currency  
    │   │   └── test_user_entity.py     # User  
    │   └── repositories/    # тесты контрактов репозиториев  
    │       ├── test_asset_repository.py # интерфейс AssetRepository  
    │       └── test_user_repository.py  # интерфейс UserRepository  
    │  
    ├── usecases/            # тесты сценариев  
    │   ├── test_calculators.py      # SMA/EMA  
    │   ├── test_get_top_assets.py   # GetTopAssetsUseCase  
    │   └── test_register_user.py    # RegisterUserUseCase  
    │  
    ├── adapters/            # тесты адаптеров  
    │   ├── test_yahoo_asset_repo.py        # YahooAssetRepository  
    │   └── test_inmemory_user_repository.py # InMemoryUserRepository  
    │  
    ├── presentation/        # тесты presentation-слоя  
    │   ├── test_utils.py         # format_table  
    │   ├── test_console.py       # console.py  
    │   ├── test_scheduler.py     # scheduler.py  
    │   └── test_auth_console.py  # auth_console.py  
    │  
    └── main/                # тесты точки входа  
        └── test_main.py     # main.py  
