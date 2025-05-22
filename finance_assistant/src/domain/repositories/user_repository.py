from abc import ABC, abstractmethod
from typing import Optional
from src.domain.entities.user import User

class UserRepository(ABC):
    """
    Контракт для хранения и поиска пользователей.
    """
    @abstractmethod
    def add_user(self, user: User) -> None:
        """Сохраняет нового пользователя."""
        raise NotImplementedError

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """Ищет пользователя по имени."""
        raise NotImplementedError
