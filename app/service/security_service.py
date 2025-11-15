from typing import List
from rich.table import Table
from rich.console import Console
from app.domain.security import Security
from app.database import get_session
from sqlalchemy.orm import Session

_console = Console()

def get_all_securities(session: Session) -> List[Security]:
    try:
        securities = session.query(Security).all()
        return securities
    finally:
        session.close()



def print_all_securities(securities: List[Security]):
    table = Table(title = "Securities")
    table.add_column("Ticker")
    table.add_column("Issuer")
    table.add_column("Price")
    for security in securities:
        table.add_row(security.ticker, security.issuer, str(security.price))
    _console.print(table)


def get_price_by_ticker(ticker: str, session: Session) -> float:
    security = session.query(Security).filter_by(ticker=ticker).one_or_none()
    if not security: 
        raise ValueError(f"Missing price for ticker '{ticker}'")
    return security.price

        
    
    # If person does not have a portfolio, prompt them to create one first
