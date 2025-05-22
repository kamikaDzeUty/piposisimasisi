from typing import Optional, Dict
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    """
    Хранилище пользователей в памяти (для разработки и тестов).
    """
    def __init__(self):
        self._storage: Dict[str, User] = {}

    def add_user(self, user: User) -> None:
        self._storage[user.username] = user

    def find_by_username(self, username: str) -> Optional[User]:
        return self._storage.get(username)
