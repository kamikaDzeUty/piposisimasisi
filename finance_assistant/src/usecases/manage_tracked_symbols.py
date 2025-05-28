from typing import List
from src.domain.repositories.user_repository import UserRepository

class ListTrackedSymbolsUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, username: str) -> List[str]:
        user = self.user_repo.find_by_username(username)
        if not user:
            raise ValueError(f"Пользователь {username!r} не найден")
        return user.tracked_symbols


class AddTrackedSymbolUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, username: str, symbol: str) -> List[str]:
        user = self.user_repo.find_by_username(username)
        if not user:
            raise ValueError(f"Пользователь {username!r} не найден")
        if symbol in user.tracked_symbols:
            raise ValueError(f"Тикер {symbol!r} уже в списке")
        user.tracked_symbols.append(symbol)
        self.user_repo.add_user(user)
        return user.tracked_symbols


class RemoveTrackedSymbolUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, username: str, symbol: str) -> List[str]:
        user = self.user_repo.find_by_username(username)
        if not user:
            raise ValueError(f"Пользователь {username!r} не найден")
        if symbol not in user.tracked_symbols:
            raise ValueError(f"Тикер {symbol!r} отсутствует в списке")
        user.tracked_symbols.remove(symbol)
        self.user_repo.add_user(user)
        return user.tracked_symbols
