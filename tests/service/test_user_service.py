
import app.service.user_service as user_service
from app.domain import User
from app.database import LocalSession
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from tabulate import tabulate
from app.service.user_service import UnsupportedUserOperationError


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


def test_get_logged_in_user():
    test_user = User(username = "X", firstname = "First", lastname = "Last", password = "Y", balance = 100.1)

    user_service._logged_in_user = test_user
    result = user_service.get_logged_in_user()
    assert result == test_user

def test_get_logged_in_user_none():
    user_service._logged_in_user = None
    result = user_service.get_logged_in_user()
    assert result == None

def test_set_logged_in_user():
    test_user = User(username = "X", firstname = "First", lastname = "Last", password = "Y", balance = 100.1)

    user_service._logged_in_user = None
    user_service.set_logged_in_user(test_user)
    assert user_service._logged_in_user == test_user

def test_set_logged_in_user_no_input():
    user_service._logged_in_user = None
    with pytest.raises(TypeError) as exc_info:
        user_service.set_logged_in_user()
    assert "missing 1 required positional argument" in str(exc_info)

def test_reset_logged_in_user():
    test_user = User(username = "X", firstname = "First", lastname = "Last", password = "Y", balance = 100.1)

    user_service._logged_in_user = test_user
    user_service.reset_logged_in_user()
    assert user_service._logged_in_user == None

def test_get_user_by_username(db_session):
    test_user = User(username = "X", firstname = "First", lastname = "Last", password = "Y", balance = 100.1)

    db_session.add(test_user)
    result = user_service.get_user_by_username("X", db_session)
    assert result == test_user

def test_get_all_users(db_session):
    test_user = User(username = "X", firstname = "First", lastname = "Last", password = "Y", balance = 100.1)
    test_user2 = User(username = "jd", firstname = "John", lastname = "Doe", password = "jd", balance = 580)

    db_session.add_all([test_user, test_user2])
    result = user_service.get_all_users(db_session)
    usernames = [u.username for u in result]

    assert "X" in usernames
    assert "jd" in usernames

def test_print_all_users(capsys, db_session):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=100.1)
    test_user2 = User(username="jd", firstname="John", lastname="Doe", password="jd", balance=580)

    db_session.add_all([test_user, test_user2])

    users = db_session.query(User).all()

    user_service.print_all_users(users)

    captured = capsys.readouterr()
    output = captured.out


    assert "X" in output
    assert "jd" in output
    assert "John" in output
    assert "First" in output
    assert "100.1" in output
    assert "580" in output

def test_create_user(db_session):
    user_data = {
        "username": "X",
        "password": "Y",
        "firstname": "First",
        "lastname": "Last",
        "balance": 100.1
    }
    result = user_service.create_user(db_session, user_data)
    user = db_session.query(User).filter_by(username = "X").one_or_none()
    assert user is not None
    assert user.firstname == "First"
    assert result == "User X created successfully"

def test_delete_user(db_session):
    test_user = User(username="testuser", firstname="Test", lastname="User", password="password", balance=1000)
    db_session.add(test_user)
    db_session.commit()

    result = user_service.delete_user(db_session, "X")
    assert result == "User X deleted successfully"

def test_delete_user_admin(db_session):
    with pytest.raises(UnsupportedUserOperationError) as exc_info:
        user_service.delete_user(db_session, "admin")
    assert "Cannot delete admin user" in str(exc_info.value)

def test_delete_user_not_exist(db_session):
    with pytest.raises(UnsupportedUserOperationError) as exc_info:
        user_service.delete_user(db_session, "nonexistentusername")
    assert "User nonexistentusername does not exist" in str(exc_info.value)


    






