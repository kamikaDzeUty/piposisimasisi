import pytest
from src.usecases.register_user import RegisterUserUseCase
from src.adapters.repositories.file_user_repository import InMemoryUserRepository
from src.domain.entities.user import User

def test_register_user_success():
    repo = InMemoryUserRepository()
    uc = RegisterUserUseCase(repo)
    # регистрация нового пользователя
    uc.execute("alice", "password", "alice@example.com")
    user = repo.find_by_username("alice")
    assert isinstance(user, User)
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.password_hash.startswith("HASHED(")

def test_register_user_duplicate_raises():
    repo = InMemoryUserRepository()
    uc = RegisterUserUseCase(repo)
    uc.execute("bob", "pw", "b@c.com")
    with pytest.raises(ValueError) as exc:
        uc.execute("bob", "other", "bob2@example.com")
    assert "Пользователь 'bob' уже есть" in str(exc.value) or "bob" in str(exc.value)
