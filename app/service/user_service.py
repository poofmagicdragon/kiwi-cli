from typing import List
from app.domain import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from rich.console import Console
from rich.table import Table
from app.database import get_session



_console = Console()

class UnsupportedUserOperationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

_logged_in_user: User|None = None

def get_logged_in_user() -> User:
    return _logged_in_user

def set_logged_in_user(user: User) -> None:
    global _logged_in_user
    _logged_in_user = user

def reset_logged_in_user() -> None:
    global _logged_in_user 
    _logged_in_user = None

def get_user_by_username(username: str, session: Session) -> User |None:
    user = session.query(User).filter_by(username=username).one_or_none()
    return user


# Function that returns all the users
def get_all_users(session: Session) -> List[User]:
    try:
        users = session.query(User).all()
        return users
    finally:
        session.close()

# Function that prints all users
def print_all_users(users: List[User]) -> None:
    table = Table(title="Users")
    table.add_column("Username", justify="center", style="cyan", no_wrap=True)
    table.add_column("First Name", justify="left", style="magenta")
    table.add_column("Last Name", justify="left", style="magenta")
    table.add_column("Balance", justify="right", style="green")
    for user in users:
        table.add_row(str(user.username), user.firstname, user.lastname, str(user.balance))
    _console.print(table)


def get_user_input() -> dict:
    try:
        balance = float(_console.input("Balance: "))
    except ValueError:
        raise UnsupportedUserOperationError("Balance must be a number.")
    return {
        "username": _console.input("Username: "),
        "password": _console.input("Password: "),
        "firstname": _console.input("First Name: "),
        "lastname": _console.input("Last Name: "),
        "balance": balance
    }
    

def create_user(session: Session, user_data: dict) -> str:
    try:
        user = User(**user_data)
        session.add(user)
        session.commit()
        return f"User {user.username} created successfully"
    except IntegrityError:
        session.rollback()
        raise UnsupportedUserOperationError(f"User with username {user_data["username"]} already exists")
    finally:
        session.close() if session else None

# def create_user_2(user: User):
#     try:
#         session = get_session()
#         session.add(user)
#         session.commit
#     finally:
#         session.close()

def get_username_for_deletion() -> str:
    username = _console.input("Username to delete: ")
    return username

def delete_user(session: Session, username: str) -> str:
    if username == "admin":
        raise UnsupportedUserOperationError("Cannot delete admin user")
    user = get_user_by_username(username, session)
    if not user:
        raise UnsupportedUserOperationError(f"User {username} does not exist")
    try:
        session.delete(user)
        session.commit()
        return f"User {username} deleted successfully"
    except IntegrityError:
        raise UnsupportedUserOperationError(f"User {username} has existing dependencies and cannot be deleted")

def update_user_balance(session: Session, username: str, new_balance: float) -> str:
    user = get_user_by_username(username, session)
    user.balance = new_balance
    session.commit()
    return f"User {username}'s balance updated successfully to {new_balance}"
