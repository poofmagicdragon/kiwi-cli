#from app.domain import security
from domain.User import User
from domain.security import Security

class Portfolio():
    def __init__(self, name:str, description: str, investment_strategy: str, user: User):
        self.id = None
        self.name = name
        self.description = description
        self.investment_strategy = investment_strategy
        self.user = user
        self.holdings = {}

    def add_security(self, security: Security, quantity: int):
        if security.ticker in self.holdings:
            self.holdings[security.ticker] += quantity
        else:
            self.holdings[security.ticker] = quantity
    
    def remove_security(self, security: Security, quantity: int):
        if security.ticker in self.holdings and self.holdings[security.ticker] >= quantity:
            self.holdings[security.ticker] -= quantity
