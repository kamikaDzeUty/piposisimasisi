from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository

class RegisterUserUseCase:
    """
    Use-case для регистрации нового пользователя.
    """
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, username: str, password: str, email: str) -> None:
        """
        1. Проверить, что username ещё не занят (user_repo.find_by_username).
        2. Захешировать пароль.inmemory_user_repository
        3. Создать User и сохранить (user_repo.add_user).
        """
        existing = self.user_repo.find_by_username(username)
        if existing:
            raise ValueError(f"Пользователь {username!r} уже есть")
        # stub: захешировать пароль
        password_hash = f"HASHED({password})"
        user = User(username=username, password_hash=password_hash, email=email)
        self.user_repo.add_user(user)
