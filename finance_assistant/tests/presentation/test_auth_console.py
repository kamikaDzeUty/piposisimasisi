import pytest
import src.presentation.auth_console as auth_mod

def test_auth_console_success(monkeypatch, capsys):
    inputs = iter(["alice", "pwd", "alice@example.com"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    # stub репозитория и usecase не нужны, InMemoryUserRepository and RegisterUserUseCase из-за заглушки всегда работают
    auth_mod.run_auth_console()
    out = capsys.readouterr().out
    assert "Пользователь успешно зарегистрирован" in out

def test_auth_console_failure(monkeypatch, capsys):
    # заставим RegisterUserUseCase.execute бросить ошибку
    class ErrUC:
        def __init__(self, repo): pass
        def execute(self, username, password, email):
            raise ValueError("duplicate")
    monkeypatch.setattr(auth_mod, "RegisterUserUseCase", ErrUC)
    monkeypatch.setattr(auth_mod, "InMemoryUserRepository", lambda: None)

    inputs = iter(["bob", "pwd", "bob@example.com"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    with pytest.raises(SystemExit) as e:
        auth_mod.run_auth_console()
    out = capsys.readouterr().out
    assert "Ошибка регистрации" in out
    assert e.value.code == 1
