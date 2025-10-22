from domain.security import Security
from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
# turn from a python class to sqlalchemy class with relationship to portfolio

class Investment(Base):
    __tablename__ = 'investment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'), nullable=False)
    ticker = Column(String(10), ForeignKey('security.ticker'), nullable=False)
    quantity = Column(Integer, nullable=False)

    portfolio = relationship("Portfolio", back_populates="investment")
    security = relationship("Security", back_populates="investment")

class PurchaseOrder():
    def __init__(self, portfolio_id:int, ticker: str, quantity: int):
        self.id = id
        self.portfolio_id = portfolio_id
        self.ticker = ticker
        self.quantity = quantity
        self.user = None
        


class SellOrder():
    def __init__(self, portfolio_id:int, ticker: str, quantity: int, sell_price: float):
        self.id = id
        self.portfolio_id = portfolio_id
        self.ticker = ticker
        self.quantity = quantity
        self.sell_price = sell_price
        self.user = None