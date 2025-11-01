#from app.domain import security
from typing import List
#from domain.User import User
from domain import User
from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

class Portfolio(Base):
    __tablename__ = 'portfolio'
    id: Mapped[int] = mapped_column(name = "id", primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    description: Mapped[str] = mapped_column(String(255), nullable = False)
    owner: Mapped[int] = mapped_column(String(30), ForeignKey("user.username"), nullable = False)

    user: Mapped["User"] = relationship("User", back_populates="portfolios")
    investments: Mapped[List["Investment"]] = relationship("Investment", back_populates = "portfolio")

    def __str__(self):
        return f"<Portfolio(name={self.name}, description={self.description}, user={self.user})>"

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
