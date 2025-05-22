from src.domain.entities.user import User

def test_user_fields():
    u = User(username="alice", password_hash="h123", email="alice@example.com")
    assert u.username == "alice"
    assert u.password_hash == "h123"
    assert u.email == "alice@example.com"
