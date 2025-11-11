from unittest import result
from rich.console import Console
from sqlalchemy import func, text
from app.domain.Portfolio import Portfolio
#from service.portfolio_service import check_if_portfolio_has_stock
from rich.table import Table
from typing import List
from app.domain.Investment import Investment
from app.database import get_session
from app.domain.security import Security
from app.service.security_service import get_price_by_ticker
from app.service.user_service import get_logged_in_user, update_user_balance
from app.service.portfolio_service import get_all_portfolio_logged_in_user
from sqlalchemy.orm import Session
from app.domain import Transaction

_console = Console()

def check_user_enough_balance(ticker: str, quantity: int, session: Session) -> bool:
    current_user = get_logged_in_user()
    price = get_price_by_ticker(ticker, session)
    if current_user.balance - (price * quantity) >= 0:
        return True
    return False

def create_purchase_order(session: Session):
    user = get_logged_in_user()
    portfolio_id = _console.input("Portfolio ID: ")
    portfolio_id = int(portfolio_id)
    if portfolio_id not in [p.id for p in get_all_portfolio_logged_in_user(session)]:
        return _console.print(f"Portfolio ID {portfolio_id} does not exist.  Please enter a valid portfolio ID", style="red")
    ticker = _console.input("Ticker: ").upper()
    quantity_to_buy = _console.input("Quantity: ")
    quantity_to_buy = int(quantity_to_buy)

    if not check_user_enough_balance(ticker, quantity_to_buy, session):
        return _console.print("Insufficient balance to make purchase", style="bold red")
    
    # This checks whether the pair of portfolio_id and ticker combination exist in database already
    exists = session.query(Investment).filter_by(portfolio_id = portfolio_id, ticker = ticker).first()
    if exists:
        exists.quantity += quantity_to_buy
    else:
        new_investment = Investment(portfolio_id=portfolio_id, ticker=ticker, quantity=quantity_to_buy)
        session.add(new_investment)
    transaction = Transaction(user_id = user.username, portfolio_id = portfolio_id, security_id = ticker, trans_type = "BUY", quantity = quantity_to_buy, price = get_price_by_ticker(ticker, session))
    session.add(transaction)

    new_balance = user.balance - (get_price_by_ticker(ticker, session) * quantity_to_buy)
    update_user_balance(session, user.username, new_balance)
    return f"Created new purchase order for {quantity_to_buy} shares of {ticker} in portfolio {portfolio_id}"

def portfolio_has_sufficient_quantity(portfolio: Portfolio, ticker: str, quantity: int) -> bool:
    if ticker in portfolio.holdings and portfolio.holdings[ticker] >= quantity:
        return True
    return False

def harvest_investment(session: Session):
    portfolio_id = _console.input("Portfolio ID: ")
    portfolio_id = int(portfolio_id)
    if portfolio_id not in [p.id for p in get_all_portfolio_logged_in_user(session)]:
        _console.print(f"Portfolio ID {portfolio_id} does not exist.  Please enter a valid portfolio ID", style="red")
        return
    try:
        portfolio_id = int(portfolio_id)
    except ValueError:
        _console.print(f"Invalid input: '{portfolio_id}' is not a number")
        return
    ticker = _console.input("Ticker: ")

    number_of_shares = session.query(func.sum(Investment.quantity)).filter_by(portfolio_id = portfolio_id, ticker = ticker).scalar()
    number_of_shares = number_of_shares or 0

    if number_of_shares == 0:
        _console.print(f"Portfolio {portfolio_id} does not have any shares of {ticker}")
        return
    quantity_to_sell = _console.input("Quantity: ")
    quantity_to_sell = int(quantity_to_sell)
    user = get_logged_in_user()

    if number_of_shares < quantity_to_sell:
        _console.print("Insufficient quantity to make sale", style="bold red")
        return
    sell_price = _console.input("Sale Price: ")
    sell_price = float(sell_price)

    number_of_shares -= quantity_to_sell
    investment = session.query(Investment).filter_by(portfolio_id = portfolio_id, ticker = ticker).first()
    investment.quantity = number_of_shares

    transaction = Transaction(user_id = user.username, portfolio_id = portfolio_id, security_id = ticker, trans_type = "SELL", quantity = quantity_to_sell, price = sell_price)
    session.add(transaction)

    new_balance = user.balance + (sell_price * quantity_to_sell)
    update_user_balance(session, user.username, new_balance)
    return f"Created and executed new sell order for {quantity_to_sell} shares of {ticker} in portfolio {portfolio_id} for ${sell_price}"

# def get_all_purchase_orders() -> List[PurchaseOrder]:
#     return db.get_all_purchase_orders()

# def print_all_purchase_orders(purchase_orders: List[PurchaseOrder]):    
#     if not purchase_orders:
#         return _console.print("No purchase orders found.", style="red")
#     table = Table(title = "Purchase Orders")
#     table.add_column("Order ID", style = "bold cyan")
#     table.add_column("Portfolio ID", style = "bold cyan")
#     table.add_column("Ticker", style = "bold cyan")
#     table.add_column("Quantity", style = "bold cyan")
#     for order in purchase_orders:
#         table.add_row(str(order.id), str(order.portfolio_id), order.ticker, str(order.quantity))
#     return _console.print(table)

def get_all_investments() -> List[Investment]:
    try:
        session = get_session()
        investments = session.query(Investment).all()
        return investments
    finally:
        session.close()

def print_all_investments() -> None:
    try:
        session = get_session()
        investments = session.query(Investment).all()
        table = Table(title = "Investments")
        table.add_column("Investment ID", style = "bold cyan")
        table.add_column("Portfolio ID", style = "bold cyan")
        table.add_column("Ticker", style = "bold cyan")
        table.add_column("Quantity", style = "bold cyan")
        for investment in investments:
            table.add_row(str(investment.id), str(investment.portfolio_id), investment.ticker, str(investment.quantity))
        _console.print(table)
    finally:
        session.close()

