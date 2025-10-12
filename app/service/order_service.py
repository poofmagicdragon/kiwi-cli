from domain.Order import PurchaseOrder, SellOrder
import db
from rich.console import Console
from domain.Portfolio import Portfolio


_console = Console()



def check_user_enough_balance(ticker: str, quantity: int) -> bool:
    current_user = db.get_logged_in_user()
    price = db.get_price_by_ticker(ticker)
    if current_user.balance - (price * quantity) >= 0:
        return True
    return False

def create_purchase_order():
    portfolio_id = _console.input("Portfolio ID: ")
    ticker = _console.input("Ticker: ")
    quantity = _console.input("Quantity: ")
    quantity = int(quantity)
    user = db.get_logged_in_user()
    portfolio = db.get_portfolio_by_id(int(portfolio_id))
    security = db.get_security_by_ticker(ticker)

    if not check_user_enough_balance(ticker, quantity):
        return _console.print("Insufficient balance to make purchase", style="bold red")
    
    purchase_order = PurchaseOrder(portfolio_id, ticker, quantity)
    db.create_new_purchase_order(purchase_order)

    new_balance = user.balance - (db.get_price_by_ticker(ticker) * quantity)
    db.update_user_balance(user, new_balance)
    portfolio.add_security(security, quantity)
    return f"Created new purchase order for {quantity} shares of {ticker} in portfolio {portfolio_id}"

def portfolio_has_sufficient_quantity(portfolio: Portfolio, ticker: str, quantity: int) -> bool:
    if ticker in portfolio.holdings and portfolio.holdings[ticker] >= quantity:
        return True
    return False

def create_sell_order():
    portfolio_id = _console.input("Portfolio ID: ")
    ticker = _console.input("Ticker: ")
    quantity = _console.input("Quantity: ")
    quantity = int(quantity)
    user = db.get_logged_in_user()
    portfolio = db.get_portfolio_by_id(int(portfolio_id))
    security = db.get_security_by_ticker(ticker)
    if not portfolio_has_sufficient_quantity(portfolio, ticker, quantity):
        return _console.print("Insufficient quantity to make sale", style="bold red")
    sell_price = _console.input("Sale Price: ")
    sell_price = float(sell_price)
    
    sell_order = SellOrder(portfolio_id, ticker, quantity, sell_price)
    db.create_new_sell_order(sell_order)

    new_balance = user.balance + (sell_price * quantity)
    db.update_user_balance(user, new_balance)
    portfolio.remove_security(security, quantity)
    return f"Created and executed new sell order for {quantity} shares of {ticker} in portfolio {portfolio_id} for ${sell_price}"




