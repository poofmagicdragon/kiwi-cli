#from app.domain import security
from domain.User import User
from domain.security import Security
from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Portfolio(Base):
    __tablename__ = 'portfolio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable = False)
    description = Column(String(500), nullable = True)
    
    investments = relationship("Investment", back_populates="portfolio")

    def __str__(self):
        user_str = getattr(self, 'user', None)
        username = user_str.username if user_str else "N/A"
        return f"<Portfolio(name={self.name}, description={self.description}, user={username})>"

    # def __init__(self, name:str, description: str, investment_strategy: str, user: User):
    #     self.id = None
    #     self.name = name
    #     self.description = description
    #     self.investment_strategy = investment_strategy
    #     self.user = user
    #     self.holdings = {}

    # def add_security(self, security: Security, quantity: int):
    #     if security.ticker in self.holdings:
    #         self.holdings[security.ticker] += quantity
    #     else:
    #         self.holdings[security.ticker] = quantity
    
    # def remove_security(self, security: Security, quantity: int):
    #     if security.ticker in self.holdings and self.holdings[security.ticker] >= quantity:
    #         self.holdings[security.ticker] -= quantity
