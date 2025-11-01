from typing import List
from domain import User
from sqlalchemy.exc import IntegrityError
#import db
from rich.console import Console
from rich.table import Table
from database import get_session

#_console = Console()

class UnsupportedUserOperation(Exception):
    def __init__(self, message: str):
        super().__init__(message)

def get_all_users() -> List[User]:
    try:
        session = get_session()
        users = session.query(User).all()
        return users
    finally:
        session.close()


print(type(User))
# # Function that returns all the users
# def get_all_users() -> List[User]:
#     try:
#         session = get_session()
#         users = session.query(User).all()
#         return users
#     finally:
#         session.close()

# # Function that prins all users
# def print_all_users(users: List[User]):
#     table = Table(title="Users")
#     table.add_column("Username", justify="center", style="cyan", no_wrap=True)
#     table.add_column("First Name", justify="left", style="magenta")
#     table.add_column("Last Name", justify="left", style="magenta")
#     table.add_column("Balance", justify="right", style="green")
#     for user in users:
#         table.add_row(str(user.username), user.firstname, user.lastname, str(user.balance))
#     _console.print(table)

    
# def create_user():
#     username = _console.input("Username: ")
#     password = _console.input("Password: ")
#     firstname = _console.input("First Name: ")
#     lastname = _console.input("Last Name: ")
#     balance = float(_console.input("Balance: "))
#     db.create_new_user(User(username, password, firstname, lastname, balance))
#     _console.print(f"User {username} created successfully", style="green")  


# def delete_user():
#     username = _console.input("Username to delete: ")
#     db.delete_user(username)
#     _console.print(f"User {username} deleted successfully", style="green")
