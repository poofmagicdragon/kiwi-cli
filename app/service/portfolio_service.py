from rich.console import Console
#from app.domain.Order import PurchaseOrder
import db
from domain.Portfolio import Portfolio
from rich.table import Table
from typing import List
from domain.security import Security

_console = Console()


def add_security_to_portfolio(portfolio: Portfolio, security: Security):
    pass

def create_portfolio():
    name = _console.input("Portfolio name: ")
    description = _console.input("Portfolio description: ")
    investment_strategy = _console.input("Investment Strategy: ")
    user = db.get_logged_in_user()
    portfolio = Portfolio(name, description, investment_strategy, user)
    db.create_new_portfolio(portfolio)
    return f"Created new portfolio {name}"

def get_all_portfolios() -> List[Portfolio]:
    return db.get_all_portfolio_logged_in_user()

def get_holdings_value(portfolio: Portfolio) -> float:
    value = 0.0
    for ticker, quantity in portfolio.holdings.items():
        security = db.get_security_by_ticker(ticker)
        if security:
            value += security.price * quantity
    return value

def print_all_portfolios(portfolios: List[Portfolio]):
    if len(portfolios) == 0:
        return _console.print("No portfolios exist.  Add new portfolios", style = "red")
        
    table = Table(title = "Portfolios")
    table.add_column("Name", style = "bold cyan")
    table.add_column("Description", style = "orchid")
    table.add_column("Investment strategy", style = "orchid")
    table.add_column("Username", style = "bold cyan")
    table.add_column("Portfolio ID", style = "orange3")
    table.add_column("Holdings", style = "bright_yellow")
    table.add_column("Holdings Value", style = "bold green")
    for portfolio in portfolios:
        table.add_row(portfolio.name, portfolio.description, portfolio.investment_strategy, portfolio.user.username, str(portfolio.id), str(portfolio.holdings), str(get_holdings_value(portfolio)))
    _console.print(table)


def delete_portfolio():
    portfolio_id = _console.input("Portfolio ID to delete: ")

    # Check if input is a valid integer
    try:
        portfolio_id_int = int(portfolio_id)
    except ValueError:
        return f"Invalid input: '{portfolio_id}' is not a numeric portfolio ID."

    portfolio = db.get_portfolio_by_id(portfolio_id_int)
    if not portfolio:
        return f"Portfolio with ID {portfolio_id_int} does not exist."

    db.delete_portfolio(portfolio)
    return f"Deleted portfolio with ID {portfolio_id_int}"

def check_if_portfolio_has_stock(portfolio: Portfolio, ticker: str) -> bool:
    if ticker in portfolio.holdings and portfolio.holdings[ticker] > 0:
        return True
    return False