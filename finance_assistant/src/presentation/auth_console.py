import sys
from src.adapters.repositories.inmemory_user_repository import InMemoryUserRepository
from src.usecases.register_user import RegisterUserUseCase

def run_auth_console():
    """
    Мини-CLI для регистрации (заглушка):
    1. Спрашиваем username, password, email
    2. Вызываем RegisterUserUseCase
    """
    print("=== Регистрация пользователя ===")
    username = input("Имя пользователя: ").strip()
    password = input("Пароль: ").strip()
    email    = input("Email: ").strip()

    repo = InMemoryUserRepository()
    uc   = RegisterUserUseCase(repo)

    try:
        uc.execute(username, password, email)
        print("Пользователь успешно зарегистрирован (stub)!")
    except Exception as e:
        print(f"Ошибка регистрации: {e}")
        sys.exit(1)
