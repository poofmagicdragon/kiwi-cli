from rich.console import Console
from app.domain.Portfolio import Portfolio
#from service.portfolio_service import check_if_portfolio_has_stock
from rich.table import Table
from typing import List
from app.domain.Investment import Investment
from app.database import get_session

_console = Console()



# def check_user_enough_balance(ticker: str, quantity: int) -> bool:
#     current_user = db.get_logged_in_user()
#     price = db.get_price_by_ticker(ticker)
#     if current_user.balance - (price * quantity) >= 0:
#         return True
#     return False

# def create_purchase_order():
#     portfolio_id = _console.input("Portfolio ID: ")
#     if portfolio_id not in [str(p.id) for p in db.get_all_portfolio_logged_in_user()]:
#         return _console.print(f"Portfolio ID {portfolio_id} does not exist.  Please enter a valid portfolio ID", style="red")
#     ticker = _console.input("Ticker: ")
#     quantity = _console.input("Quantity: ")
#     quantity = int(quantity)
#     user = db.get_logged_in_user()
#     portfolio = db.get_portfolio_by_id(int(portfolio_id))
#     security = db.get_security_by_ticker(ticker)

#     if not check_user_enough_balance(ticker, quantity):
#         return _console.print("Insufficient balance to make purchase", style="bold red")
    
#     purchase_order = PurchaseOrder(portfolio_id, ticker, quantity)
#     db.create_new_purchase_order(purchase_order)

#     new_balance = user.balance - (db.get_price_by_ticker(ticker) * quantity)
#     db.update_user_balance(user, new_balance)
#     portfolio.add_security(security, quantity)
#     return f"Created new purchase order for {quantity} shares of {ticker} in portfolio {portfolio_id}"

# def portfolio_has_sufficient_quantity(portfolio: Portfolio, ticker: str, quantity: int) -> bool:
#     if ticker in portfolio.holdings and portfolio.holdings[ticker] >= quantity:
#         return True
#     return False

# def create_sell_order():
#     portfolio_id = _console.input("Portfolio ID: ")
#     if portfolio_id not in [str(p.id) for p in db.get_all_portfolio_logged_in_user()]:
#         return _console.print(f"Portfolio ID {portfolio_id} does not exist.  Please enter a valid portfolio ID", style="red")
#     try:
#         portfolio_id = int(portfolio_id)
#     except ValueError:
#         return _console.print(f"Invalid input: '{portfolio_id}' is not a number")
#     ticker = _console.input("Ticker: ")
#     if not check_if_portfolio_has_stock(db.get_portfolio_by_id(portfolio_id), ticker):
#         return _console.print(f"Portfolio {portfolio_id} does not have any shares of {ticker}")
#     quantity = _console.input("Quantity: ")
#     quantity = int(quantity)
#     user = db.get_logged_in_user()
#     portfolio = db.get_portfolio_by_id(int(portfolio_id))
#     security = db.get_security_by_ticker(ticker)
#     if not portfolio_has_sufficient_quantity(portfolio, ticker, quantity):
#         return _console.print("Insufficient quantity to make sale", style="bold red")
#     sell_price = _console.input("Sale Price: ")
#     sell_price = float(sell_price)
    
#     sell_order = SellOrder(portfolio_id, ticker, quantity, sell_price)
#     db.create_new_sell_order(sell_order)

#     new_balance = user.balance + (sell_price * quantity)
#     db.update_user_balance(user, new_balance)
#     portfolio.remove_security(security, quantity)
#     return f"Created and executed new sell order for {quantity} shares of {ticker} in portfolio {portfolio_id} for ${sell_price}"

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