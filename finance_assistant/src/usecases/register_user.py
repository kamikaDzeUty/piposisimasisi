# src/usecases/register_user.py

import re
import bcrypt
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository

EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")

class RegisterUserUseCase:
    """
    Use-case для регистрации пользователя.
    Проверяет:
      - уникальность username,
      - совпадение password и password2,
      - минимальную длину пароля,
      - корректность e-mail.
    Хеширует пароль через bcrypt и сохраняет через репозиторий.
    """
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(
        self,
        username: str,
        password: str,
        password2: str,
        email: str
    ) -> None:
        # 1) Проверяем, что логин свободен
        if self.user_repo.find_by_username(username):
            raise ValueError(f"Пользователь {username!r} уже существует")

        # 2) Пароли совпадают?
        if password != password2:
            raise ValueError("Пароли не совпадают")

        # 3) Минимальная длина пароля
        if len(password) < 6:
            raise ValueError("Пароль слишком короткий (минимум 6 символов)")

        # 4) Формат e-mail
        if not EMAIL_RE.fullmatch(email):
            raise ValueError("Неверный формат e-mail")

        # 5) Хешируем и сохраняем
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(
            username=username,
            password_hash=password_hash,
            email=email
        )
        self.user_repo.add_user(user)
