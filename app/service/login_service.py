from typing import Tuple
from rich.console import Console
from app.database import get_session
from app.domain.User import User
from sqlalchemy.orm import Session
from app.service.user_service import set_logged_in_user, get_logged_in_user

_console = Console()

def login(username: str, password: str, session: Session) -> None:
    # username, password = get_login_inputs()
    # session = get_session()
    user = session.query(User).filter(User.username == username).first()
    if not user or str(user.password) != password:
        raise Exception("Error: Login failed")
    set_logged_in_user(user)
    print(f"Login Successful.  Hello {get_logged_in_user().username}")


def get_login_inputs() -> Tuple[str, str]:
    username = _console.input("Username: ")
    password = _console.input("Password: ")
    return username, password

