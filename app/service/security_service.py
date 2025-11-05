from typing import List
from rich.table import Table
from rich.console import Console
from app.domain.security import Security
from app.database import get_session

_console = Console()

def get_all_securities() -> List[Security]:
    try:
        session = get_session()
        securities = session.query(Security).all()
        return securities
    finally:
        session.close()



def print_all_securities(securities: List[Security]):
    try:
        session = get_session()
        securities = session.query(Security).all()
        table = Table(title = "Securities")
        table.add_column("Ticker")
        table.add_column("Issuer")
        table.add_column("Price")
        for security in securities:
            table.add_row(security.ticker, security.issuer, str(security.price))
        _console.print(table)
    finally:
        session.close()


    # If person does not have a portfolio, prompt them to create one first
