import json
from pathlib import Path
from typing import Optional
from json.decoder import JSONDecodeError

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository

class FileUserRepository(UserRepository):
    """
    Хранит пользователей в JSON-файле (users.json).
    """

    def __init__(self, path: Path = Path("users.json")):
        self.path = path
        self.users: dict[str, User] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists() or self.path.stat().st_size == 0:
            self.users = {}
            return

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self.users = {}
            for u in raw:
                self.users[u["username"]] = User(
                    username=u["username"],
                    password_hash=u["password_hash"],
                    email=u["email"],
                    tracked_symbols=u.get("tracked_symbols", []),
                )
        except (JSONDecodeError, KeyError, TypeError):
            self.users = {}

    def _save(self) -> None:
        payload = []
        for u in self.users.values():
            payload.append({
                "username": u.username,
                "password_hash": u.password_hash,
                "email": u.email,
                "tracked_symbols": u.tracked_symbols
            })
        # сохраняем с ensure_ascii=False, чтобы не крашились юникод
        self.path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def add_user(self, user: User) -> None:
        self.users[user.username] = user
        self._save()

    def find_by_username(self, username: str) -> Optional[User]:
        return self.users.get(username)
