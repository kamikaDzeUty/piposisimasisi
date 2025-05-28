import pytest

from src.adapters.repositories.file_user_repository import InMemoryUserRepository
from src.domain.entities.user import User


def test_inmemory_add_and_find_user():
    repo = InMemoryUserRepository()
    # до добавления пользователя — None
    assert repo.find_by_username("alice") is None

    user = User(username="alice", password_hash="hash1", email="alice@example.com")
    repo.add_user(user)

    found = repo.find_by_username("alice")
    assert found is user

    # поиск несуществующего по-прежнему None
    assert repo.find_by_username("bob") is None


def test_inmemory_overwrite_user():
    repo = InMemoryUserRepository()
    user1 = User(username="u", password_hash="h1", email="e1")
    user2 = User(username="u", password_hash="h2", email="e2")
    repo.add_user(user1)
    repo.add_user(user2)
    # последняя запись перезаписала первую
    found = repo.find_by_username("u")
    assert found is user2
