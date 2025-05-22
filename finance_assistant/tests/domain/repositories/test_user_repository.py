import pytest
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository

class DummyUserRepo(UserRepository):
    def add_user(self, user: User):
        # stub
        self._last = user
    def find_by_username(self, username: str):
        return getattr(self, "_last", None)

def test_cannot_instantiate_user_repository_directly():
    with pytest.raises(TypeError):
        UserRepository()

def test_dummy_user_repository_add_and_find():
    repo = DummyUserRepo()
    user = User("bob", "hash", "bob@example.com")
    repo.add_user(user)
    found = repo.find_by_username("bob")
    assert found is user
