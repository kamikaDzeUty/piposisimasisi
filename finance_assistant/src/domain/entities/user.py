from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    """
    Доменная сущность «Пользователь»
    хранит логин, хеш пароля, e-mail и список отслеживаемых тикеров.
    """
    username: str
    password_hash: str
    email: str
    tracked_symbols: List[str] = field(default_factory=list)
