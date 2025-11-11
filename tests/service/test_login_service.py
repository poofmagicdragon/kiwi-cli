
from app.service.login_service import get_login_inputs, login
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
import pytest
from app.domain.User import User


# mock db setup here 
test_engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(test_engine)
TestSessionLocal = sessionmaker(bind = test_engine)


# this runs before each test function
@pytest.fixture
def db_session():
    session = TestSessionLocal()
    yield session
    session.rollback()
    session.close()

def test_login(monkeypatch, db_session):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=100.1)
    test_user2 = User(username="jd", firstname="John", lastname="Doe", password="jd", balance=580)
    db_session.add_all([test_user, test_user2])
    user1 = db_session.query(User).filter_by(username = "X").one_or_none()

    inputs = iter(["X", "Y"])
    monkeypatch.setattr("app.service.login_service._console.input", lambda _: next(inputs))
    username, password = get_login_inputs()
    login(username, password, db_session)    

    assert user1 is not None
    assert user1.username == "X"
    assert user1.password == "Y"

def test_login_wrong_password(monkeypatch, db_session):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=100.1)
    test_user2 = User(username="jd", firstname="John", lastname="Doe", password="jd", balance=580)
    db_session.add_all([test_user, test_user2])
    user1 = db_session.query(User).filter_by(username = "X").one_or_none()

    inputs = iter(["X", "wrongpassword"])
    monkeypatch.setattr("app.service.login_service._console.input", lambda _: next(inputs))
    username, password = get_login_inputs()  

    with pytest.raises(Exception) as exc_info:
        login(username, password, db_session)  
    
    assert "Error: Login failed" in str(exc_info.value)

def test_get_login_inputs(monkeypatch):
    inputs = iter(["testuser", "testpass"])
    monkeypatch.setattr("app.service.login_service._console.input", lambda _: next(inputs))
    username, password = get_login_inputs()
    assert username == "testuser"
    assert password == "testpass"

