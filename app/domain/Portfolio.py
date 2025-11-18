#from app.domain import security
from typing import List
# from app.domain import Transaction, User, Investment
from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped

class Portfolio(Base):
    __tablename__ = 'portfolio'
    id: Mapped[int] = mapped_column(name = "id", primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    description: Mapped[str] = mapped_column(String(255), nullable = False)
    investment_strategy: Mapped[str] = mapped_column(String(255), nullable = False)
    owner: Mapped[int] = mapped_column(String(30), ForeignKey("user.username"), nullable = False)

    user: Mapped["User"] = relationship("User", back_populates="portfolios")
    investments: Mapped[List["Investment"]] = relationship("Investment", back_populates = "portfolio")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="portfolio")
    
    def __str__(self):
        return f"<Portfolio(name={self.name}, description={self.description}, user={self.owner})>"

    

