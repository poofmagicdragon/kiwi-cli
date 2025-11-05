from typing import Tuple
from rich.console import Console
from app.database import get_session
from app.domain.User import User

_console = Console()

def login():
    username, password = get_login_inputs()
    session = get_session()
    user = session.query(User).filter(User.username == username).first()
    if not user or str(user.password) != password:
        raise Exception("Error: Login failed")
    #db.set_logged_in_user(user)


def get_login_inputs() -> Tuple[str, str]:
    username = _console.input("Username: ")
    password = _console.input("Password: ")
    return username, password

