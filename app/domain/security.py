from database import Base
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship

class Security(Base):
    __tablename__ = 'security'
    ticker = Column(String(10), primary_key=True)
    issuer = Column(String(100), nullable = False)
    price = Column(Float, nullable = False)

    investments = relationship("Investment", back_populates="security")

    # def __init__(self, ticker: str, issuer: str, price: float):
    #     self.ticker = ticker
    #     self.issuer = issuer
    #     self.price = price