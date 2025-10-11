from domain.User import User
from typing import Dict, List
from domain.security import Security
from domain.Portfolio import Portfolio


class UniqueConstraintError(Exception):
     def __init__(self, message: str):
         super().__init__(message)

_portfolio_id: int = 0 

_users: Dict[str, User] = {
    "admin": User("admin", "adminpass", "Admin Firstname", "Admin Lastname", 0.0)
}

_securities:Dict[str, Security] = {
    "AAPL": Security("AAPL", "AAPL INC.", 100.00),
    "FB": Security("FB", "FaceBook", 112.00),
    "MFST": Security("MFST", "Microsoft Corp.", 80.00)
}

_portfolios: Dict[int, Portfolio] = {

}

_logged_in_user: User|None = None


def get_logged_in_user():
    return _logged_in_user

def set_logged_in_user(user: User):
    global _logged_in_user # anti-pattern but ok for this simple app
    _logged_in_user = user


def reset_logged_in_user():
    global _logged_in_user 
    _logged_in_user = None


def query_user(username:str) -> User|None:
    try:
        return _users[username]
    except KeyError as ke:
        return None

def query_all_users() -> list[User]:
    return list(_users.values())

def create_new_user(user: User):
    if user.username in _users:
        raise UniqueConstraintError(f"User with username {user.username} already exists")
    _users[user.username] = user

def delete_user(username: str):
    if username not in _users:
        raise Exception(f"User with username {username} does not exist")
    if username == "admin":
        raise Exception("Cannot delete admin user")
    del _users[username]



    # CRUD operations on securities Create, Read, Update (not supported), Delete (not supported)
def get_all_securities() -> List[Security]:
    return list(_securities.values())

def get_all_portfolios() -> List[Portfolio]:
    return list(_portfolios.values())

def get_all_portfolio_logged_in_user() -> List[Portfolio]:
    user_portfolios = []
    for portfolio in get_all_portfolios():
        if portfolio.user.username == _logged_in_user.username:
            user_portfolios.append(portfolio)
    return user_portfolios    

def create_new_portfolio(portfolio: Portfolio):
    global _portfolio_id
    _portfolio_id += 1
    portfolio.id = _portfolio_id
    _portfolios[_portfolio_id] = portfolio

def increment_portfolio_id():
    global _portfolio_id
    _portfolio_id = _portfolio_id + 1
