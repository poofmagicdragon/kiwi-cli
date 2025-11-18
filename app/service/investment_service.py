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
from app.domain import Transaction, User

_console = Console()

def check_user_enough_balance(ticker: str, quantity: int, session: Session, current_user: User) -> bool:
    price = get_price_by_ticker(ticker, session)
    if current_user.balance - (price * quantity) >= 0:
        return True
    return False

def create_purchase_order(session: Session, user: User) -> str:
    portfolio_id = _console.input("Portfolio ID: ")
    portfolio_id = int(portfolio_id)
    if portfolio_id not in [p.id for p in get_all_portfolio_logged_in_user(session)]:
        _console.print(f"Portfolio ID {portfolio_id} does not exist.  Please enter a valid portfolio ID", style="red")
        return f"Portfolio ID {portfolio_id} does not exist.  Please enter a valid portfolio ID"
    ticker = _console.input("Ticker: ").upper()
    quantity_to_buy = _console.input("Quantity: ")
    quantity_to_buy = int(quantity_to_buy)

    if not check_user_enough_balance(ticker, quantity_to_buy, session, user):
        _console.print("Insufficient balance to make purchase", style="bold red")
        return "Insufficient balance to make purchase"
    
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

def portfolio_has_sufficient_quantity(portfolio: Portfolio, ticker: str, quantity: int, session: Session) -> bool:
    investment = session.query(Investment).filter_by(portfolio_id = portfolio.id, ticker = ticker).first()
    if investment and investment.quantity >= quantity:
        return True
    return False

def harvest_investment(session: Session, user: User) -> str:
    portfolio_id = _console.input("Portfolio ID: ")
    
    try:
        portfolio_id = int(portfolio_id)
    except ValueError:
        _console.print(f"Invalid input: '{portfolio_id}' is not a number")
        return f"Invalid input: '{portfolio_id}' is not a number"
    
    if portfolio_id not in [p.id for p in get_all_portfolio_logged_in_user(session)]:
        _console.print(f"Portfolio ID {portfolio_id} does not exist.  Please enter a valid portfolio ID", style="red")
        return f"Portfolio ID {portfolio_id} does not exist.  Please enter a valid portfolio ID"
    ticker = _console.input("Ticker: ")

    number_of_shares = session.query(func.sum(Investment.quantity)).filter_by(portfolio_id = portfolio_id, ticker = ticker).scalar()
    number_of_shares = number_of_shares or 0

    if number_of_shares == 0:
        _console.print(f"Portfolio {portfolio_id} does not have any shares of {ticker}")
        return f"Portfolio {portfolio_id} does not have any shares of {ticker}"
    quantity_to_sell = _console.input("Quantity: ")
    quantity_to_sell = int(quantity_to_sell)
 

    if number_of_shares < quantity_to_sell:
        _console.print("Insufficient quantity to make sale", style="bold red")
        return "Insufficient quantity to make sale"
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
