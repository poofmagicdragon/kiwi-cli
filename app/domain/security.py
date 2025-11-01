from database import Base
from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Security(Base):
    __tablename__ = 'security'

    ticker: Mapped[str] = mapped_column(String(10), primary_key=True)
    issuer: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    investments: Mapped[List["Investment"]] = relationship("Investment", back_populates="security")

    # def __init__(self, ticker: str, issuer: str, price: float):
    #     self.ticker = ticker
    #     self.issuer = issuer
    #     self.price = price