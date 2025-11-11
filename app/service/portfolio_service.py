from pytest import Session
from rich.console import Console
from app.domain import Investment, User
from app.domain.Portfolio import Portfolio
from rich.table import Table
from typing import List
from sqlalchemy.exc import IntegrityError
from app.domain.security import Security 
from app.service.user_service import get_logged_in_user
from app.database import get_session


_console = Console()

class UnsupportedUserOperationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

# def add_security_to_portfolio(portfolio: Portfolio, security: Security):
#     pass


def create_portfolio(session: Session, user: User) -> str:
    try:
        name = _console.input("Portfolio name: ")
        description = _console.input("Portfolio description: ")
        investment_strategy = _console.input("Investment Strategy: ")
        session.add(Portfolio(owner = user.username, name = name, description = description, investment_strategy = investment_strategy))
        session.commit()
        return f"Portfolio {name} created successfully"
    finally:
        session.close()
    
def get_portfolio_by_name(name: str, session: Session) -> Portfolio |None:
    portfolio = session.query(Portfolio).filter_by(name=name).one_or_none()
    return portfolio


def get_all_portfolios(session: Session) -> List[Portfolio]:
    try:
        portfolios = session.query(Portfolio).all()
        return portfolios
    finally:
        session.close()


# def get_holdings_value(portfolio: Portfolio) -> float:
#     value = 0.0
#     for ticker, quantity in portfolio.holdings.items():
#         security = db.get_security_by_ticker(ticker)
#         if security:
#             value += security.price * quantity
#     return value

def print_all_portfolios(session: Session):    
    try:
        portfolios = session.query(Portfolio).filter_by(owner = get_logged_in_user().username).all()
        if len(portfolios) == 0:
            return _console.print("No portfolios exist.  Add new portfolios", style = "red")    
        
        table = Table(title = "Portfolios")
        table.add_column("Portfolio ID", style = "orange3")
        table.add_column("Owner", style = "bold cyan")
        table.add_column("Name", style = "bold cyan")
        table.add_column("Description", style = "orchid")
        table.add_column("Investment strategy", style = "orchid")
        #table.add_column("Holdings value", style = "green")
        table.add_column("Investments", style = "green")


        for portfolio in portfolios:
            investments = session.query(Investment).filter_by(portfolio_id=portfolio.id).all()
            investment_dicts = [{"ticker": inv.ticker, "quantity": inv.quantity,} for inv in investments]
            investments_str = ", ".join(f"{inv['ticker']} ({inv['quantity']})" for inv in investment_dicts)
            
            table.add_row(str(portfolio.id), portfolio.owner, portfolio.name, portfolio.description, portfolio.investment_strategy, investments_str)
        _console.print(table)
    finally:
        session.close()


def delete_portfolio(session: Session, portfolio_name: str) -> str:
    try:
        portfolio = get_portfolio_by_name(portfolio_name, session)

        if portfolio is None:
            raise UnsupportedUserOperationError(f"Portfolio '{portfolio_name}' does not exist")
        session.delete(portfolio)
        session.commit()
        return f"Portfolio '{portfolio_name}' deleted successfully"
    except IntegrityError:
        raise UnsupportedUserOperationError(f"Portfolio '{portfolio_name}' has existing dependencies and cannot be deleted")
    

def get_all_portfolio_logged_in_user(session: Session) -> List[Portfolio]:
    user = get_logged_in_user()
    portfolios = session.query(Portfolio).filter_by(owner = user.username).all()
    return portfolios

# def check_if_portfolio_has_stock(portfolio: Portfolio, ticker: str) -> bool:
#     if ticker in portfolio.holdings and portfolio.holdings[ticker] > 0:
#         return True
#     return False