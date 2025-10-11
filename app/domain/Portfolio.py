from domain.User import User
from domain.security import Security

class Portfolio():
    def __init__(self, name:str, description: str, investment_strategy: str, user: User):
        self.id = None
        self.name = name
        self.description = description
        self.investment_strategy = investment_strategy
        self.user = user

def add_security(self, security: Security, quantity: int):
    if self.holdings:
        if self.holdings[security.ticker]:
            self.holdings[security.ticker] += quantity 
    else:
        self.holdings = [security]
    