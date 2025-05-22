from abc import ABC
from dataclasses import dataclass

@dataclass
class User(ABC):
    """
    Доменная сущность «Пользователь».
    """
    username: str
    password_hash: str
    email: str
