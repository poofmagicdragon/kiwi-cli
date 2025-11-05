from typing import Dict, Tuple, List
from rich.console import Console
from app.cli import constants
from app.domain.MenuFunctions import MenuFunctions
import sys
from rich.table import Table
from app.service.login_service import login
from app.service.user_service import get_all_users, print_all_users, create_user, delete_user, get_logged_in_user, reset_logged_in_user
from app.service.portfolio_service import create_portfolio, get_all_portfolios, print_all_portfolios, delete_portfolio
from app.service.security_service import get_all_securities, print_all_securities
#from app.service.investment_service import create_purchase_order, create_sell_order, print_all_purchase_orders, get_all_purchase_orders


_console = Console()

class UnsupportedMenuError(Exception):
    def __init__ (self, message:str):
        super().__init__(message)

_menus: Dict[int, str] = {
    constants.LOGIN_MENU: "----\nWelcome to Kiwi\n----\n1. Login\n0. Exit",
    constants.MAIN_MENU: "----\nMain Menu\n----\n1. Manage Users\n2. Manage portfolios\n3. Market place\n0. Logout",
    constants.MANAGE_USERS_MENU: "----\nManage Users\n----\n1. View users\n2. Add user\n3. Delete user\n0. Back to main menu",
    constants.MANAGE_PORTFOLIO: "----\nPortfolio Menu\n----\n1. View portfolio\n2. Create portfolio\n3. Delete Portfolio\n4. Harvest Investment\n0. Back to main menu",
    constants.MARKET_PLACE: "----\nMarketplace\n----\n1. View securities\n2. Place purchase order\n3. View Purchase Orders\n0. Back to main menu"
}

# for purchase order
# the app should prompt for: Ticker, quantity, portfolio_id
# app should check whether there is sufficient balance for the transaction
# if not an error then query portfolio that matches the user provided id
# add the security to that portfolio
# print a success message

# for sell order
# user will be prompted for a portfolio id, ticker of security to sell, quantity to sell, price to sell
# check if the quantity to be sold is greater than the quantity owned in the portfolio
# to do that we need to query the portfolio, get quantity of given investment, compare to sale order
# if valid letthe sale go through and update the balance (add sale proceeds - sale price * quantity - to user balance)
# update the portfolio security quantity to reflect this sale order

# example:
# User (username: "mt", ... balance = 1000)
# Portfolio (id: 1, name : "2025 Tech", ...)
# place a purchase order
# user selects: portfolio id =1, ticker = AAPL, quantity = 10
# check balance: required fund = 10 * 100 = 1000 <= user balance -> let the order through
# New objects after the order is complete:
# User: [username: "mt", ... balance = 0]
# portfolio [id: 1, name: "2025 Tech", ..., holdings = {AAPL: 10}]
# --> place an investment liquidation order
# prompt user for: portfolio id(1), ticker(AAPL), quantity (5), sale_price (120)
# 1. check if quantity is valid: portfolio.holdings[AAPL] => quantity -> quantity is valid
# new user balance = existing balance + sale proceeds (120*5 = 600)
# After the purchase order:
# Portfolio: [id: 1, name: "2025 Tech", ..., holdings = {AAPL: 5}]
# User: [username: "mt", ... balance = 600]

def navigate_to_manage_user_menu() -> int:
    logged_in_user = get_logged_in_user()
    if logged_in_user and logged_in_user.username != "admin":
        raise UnsupportedMenuError("Only admin user can manage users")
    return constants.MANAGE_USERS_MENU

#purpose: to define the functions that needs to be executed depending on the user selection
# user selection depends on the menu
_router: Dict[str, MenuFunctions] = {
    "0.1": MenuFunctions(executor = login, navigator = lambda: constants.MAIN_MENU),
    "1.1": MenuFunctions(navigator = navigate_to_manage_user_menu),
    "1.2": MenuFunctions(navigator = lambda: constants.MANAGE_PORTFOLIO),
    "2.1": MenuFunctions(executor = get_all_users, printer = print_all_users, navigator = lambda: constants.MANAGE_USERS_MENU),
    "2.2": MenuFunctions(executor = create_user, printer = lambda x: _console.print(f'\n{x}')), # add user
    "2.3": MenuFunctions(executor = delete_user, printer = lambda x: _console.print(f'\n{x}')), 
    "1.3": MenuFunctions(navigator = lambda: constants.MARKET_PLACE),
    "4.1": MenuFunctions(executor= get_all_securities, printer = print_all_securities),
    "3.1": MenuFunctions(executor = get_all_portfolios, printer = print_all_portfolios),
    "3.2": MenuFunctions(executor = create_portfolio, printer = lambda x: _console.print(f'\n{x}')),
    #"4.2": MenuFunctions(executor = create_purchase_order, printer = lambda x: _console.print(f'\n{x}')),
    "3.3": MenuFunctions(executor = delete_portfolio, printer = lambda x: _console.print(f'\n{x}')),
    #"3.4": MenuFunctions(executor = create_sell_order, printer = lambda x: _console.print(f'\n{x}')),
    #"4.3": MenuFunctions(executor = get_all_purchase_orders, printer = print_all_purchase_orders)
}





def print_error(error: str):
    _console.print(error, style = "red")


def handle_user_selection(menu_id: int, user_selection: int):
    if user_selection == 0:
        if menu_id == constants.LOGIN_MENU:
            sys.exit(0) # terminate application
        if menu_id == constants.MAIN_MENU:
            reset_logged_in_user()
            print_menu(constants.LOGIN_MENU)
        else:
            print_menu(constants.MAIN_MENU)
    formatted_user_input = f"{str(menu_id)}.{str(user_selection)}"
    menu_functions = _router.get(formatted_user_input)

    # When a user inputs a selection that isn't on the menu, show them this text and keep them on the same page
    if not menu_functions:
        print_error(f"Error: {user_selection} is not a valid option")
        print_menu(menu_id)
        

    try:
        if menu_functions.executor:
            result = menu_functions.executor()
            if menu_functions.printer:
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






