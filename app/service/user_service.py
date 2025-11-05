from typing import List
from app.domain import User
from sqlalchemy.exc import IntegrityError
from rich.console import Console
from rich.table import Table
from app.database import get_session

_console = Console()

class UnsupportedUserOperationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

_logged_in_user: User|None = None

def get_logged_in_user():
    return _logged_in_user

def set_logged_in_user(user: User):
    global _logged_in_user
    _logged_in_user = user

def reset_logged_in_user():
    global _logged_in_user 
    _logged_in_user = None

def get_user_by_username(username: str) -> User |None:
    try:
        session = get_session()
        user = session.query(User).filter_by(username=username).one_or_none()
        return user
    finally:
        session.close()

# Function that returns all the users
def get_all_users() -> List[User]:
    try:
        session = get_session()
        users = session.query(User).all()
        return users
    finally:
        session.close()

# Function that prints all users
def print_all_users() -> None:
    try:
        session = get_session()
        users = session.query(User).all()
        table = Table(title="Users")
        table.add_column("Username", justify="center", style="cyan", no_wrap=True)
        table.add_column("First Name", justify="left", style="magenta")
        table.add_column("Last Name", justify="left", style="magenta")
        table.add_column("Balance", justify="right", style="green")
        for user in users:
            table.add_row(str(user.username), user.firstname, user.lastname, str(user.balance))
        _console.print(table)
    finally:
        session.close()

    
def create_user():
    try:
        username = _console.input("Username: ")
        password = _console.input("Password: ")
        firstname = _console.input("First Name: ")
        lastname = _console.input("Last Name: ")
        balance = float(_console.input("Balance: "))
        session = get_session()
        session.add(User(username=username, password=password, firstname=firstname, lastname=lastname, balance=balance))
        session.commit()
        return f"User {username} created successfully"
    except ValueError:
        raise UnsupportedUserOperationError("Invalid input. Please try again.") # This is for balance 
    except IntegrityError:
        raise UnsupportedUserOperationError(f"User with username {username} already exists")
    finally:
        session.close() if session else None

def create_user_2(user: User):
    try:
        session = get_session()
        session.add(user)
        session.commit
    finally:
        session.close()

def delete_user():
    session = None
    try:
        username = _console.input("Username to delete: ")
        if username == "admin":
            raise UnsupportedUserOperationError("Cannot delete admin user")
        user = get_user_by_username(username)
        session = get_session()
        session.delete(user)
        session.commit()
        return f"User {username} delete successfully"
    except UnsupportedUserOperationError as e:
        raise e
    except IntegrityError:
        raise UnsupportedUserOperationError(f"User {username} has existing dependencies and cannot be deleted")
    finally:
        session.close() if session else None
