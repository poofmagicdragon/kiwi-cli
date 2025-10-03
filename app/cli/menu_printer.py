from typing import Dict, Tuple, List
from rich.console import Console
from cli import constants
from domain.MenuFunctions import MenuFunctions
import db
import sys
from domain.User import User
from rich.table import Table

class UnsupportedMenuError(Exception):
    def __init__ (self, message:str):
        super().__init__(message)


_console = Console()

_menus: Dict[int, str] = {
    constants.LOGIN_MENU: "----\nWelcome to Kiwi\n----\n1. Login\n0. Exit",
    constants.MAIN_MENU: "----\nMain Menu\n----\n1. Manage Users\n2. Manage portfolios\n3. Market place\n0. Logout",
    constants.MANAGE_USERS_MENU: "----\nManage Users\n----\n1. View users\n2. Add user\n3. Delete user\n0. Back to main menu"
}



def get_login_inputs() -> Tuple[str, str]:
    username = _console.input("Username: ")
    password = _console.input("Password: ")
    return username, password

# throw an error if login failed, return nothing otherwise
def login():
    username, password = get_login_inputs()
    user = db.query_user(username)
    # if not user:
    #     raise Exception("Username is incorrect")
    # else: 
    #     if user.password == password:
    #         print_menu(constants.MAIN_MENU)
    #     else:
    #         print_error("Error: Login failed")
    #         print_menu(constants.LOGIN_MENU)
    if not user or user.password != password:
        raise Exception("Error: Login failed")
    db.set_logged_in_user(user)


# Function that returns all the users
def get_all_users() -> List[User]:
    return db.query_all_users()

# Function that prins all users
def print_all_users(users: List[User]):
    table = Table(title="Users")
    table.add_column("Username", justify="center", style="cyan", no_wrap=True)
    table.add_column("First Name", justify="left", style="magenta")
    table.add_column("Last Name", justify="left", style="magenta")
    table.add_column("Balance", justify="right", style="yellow")
    for user in users:
        table.add_row(str(user.username), user.firstname, user.lastname, str(user.balance))
    _console.print(table)

    
def create_user():
    username = _console.input("Username: ")
    password = _console.input("Password: ")
    firstname = _console.input("First Name: ")
    lastname = _console.input("Last Name: ")
    balance = float(_console.input("Balance: "))
    db.create_new_user(User(username, password, firstname, lastname, balance))
    _console.print(f"User {username} created successfully", style="green")  


def delete_user():
    username = _console.input("Username to delete: ")
    db.delete_user(username)
    _console.print(f"User {username} deleted successfully", style="green")

def navigate_to_manage_user_menu() -> int:
    logged_in_user = db.get_logged_in_user()
    if logged_in_user and logged_in_user.username != "admin":
        raise UnsupportedMenuError("Only admin user can manage users")
    return constants.MANAGE_USERS_MENU

#purpose: to define the functions that needs to be executed depending on the user selection
# user selection depends on the menu
_router: Dict[str, MenuFunctions] = {
    "0.1": MenuFunctions(executor = login, navigator = lambda: constants.MAIN_MENU),
    "1.1": MenuFunctions(navigator = navigate_to_manage_user_menu),
    "2.1": MenuFunctions(executor = get_all_users, printer = print_all_users, navigator = lambda: constants.MANAGE_USERS_MENU),
    "2.2": MenuFunctions(executor = create_user, printer = lambda x: _console.print(f'\n{x}')), # add user
    "2.3": MenuFunctions(executor = delete_user, printer = lambda x: _console.print(f'\n{x}'))
}

#1. 
#2. 
#3. 



def print_error(error: str):
    _console.print(error, style = "red")


def handle_user_selection(menu_id: int, user_selection: int):
    if user_selection == 0:
        if menu_id == constants.LOGIN_MENU:
            sys.exit(0) # terminate application
        if menu_id == constants.MAIN_MENU:
            db.reset_logged_in_user
            print_menu(constants.LOGIN_MENU)
        else:
            print_menu(constants.MAIN_MENU)
    formatted_user_input = f"{str(menu_id)}.{str(user_selection)}"
    menu_functions = _router[formatted_user_input]
    try:
        if menu_functions.executor:
            result = menu_functions.executor()
            if result and menu_functions.printer:
                menu_functions.printer(result)
        if menu_functions.navigator:
            print_menu(menu_functions.navigator())
        else:
            print_menu(menu_id)
    except Exception as e:
        print_error(str(e))
        print_menu(menu_id)



def print_menu(menu_id: int):
    _console.print(_menus[menu_id])
    user_selection = int(_console.input(">>"))
    handle_user_selection(menu_id, user_selection)






