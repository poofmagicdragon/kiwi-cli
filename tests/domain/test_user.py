from app.domain.User import User, __str__

def test_user_representation():
    user = User(username="testuser", password="password", firstname="Test", lastname="User", balance=1000.0)

    result = user.__str__()
    assert result == "User(username='testuser', firstname='Test User', balance=1000.0)"