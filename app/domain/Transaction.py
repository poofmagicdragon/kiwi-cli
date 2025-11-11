#from app.domain import security
from typing import List
# from app.domain import Portfolio, User, Security
from app.database import Base
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import UTC, datetime


class Transaction(Base):
    __tablename__ = 'transaction'
    id: Mapped[int] = mapped_column(name = "id", primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("user.username"), nullable = False)
    portfolio_id: Mapped[int] = mapped_column(Integer, ForeignKey("portfolio.id"), nullable = False)
    security_id: Mapped[str] = mapped_column(ForeignKey("security.ticker"), nullable = False)
    trans_type: Mapped[str] = mapped_column(String(6), nullable = False)
    quantity: Mapped[int] = mapped_column(Integer, nullable = False)
    price: Mapped[float] = mapped_column(Float, nullable = False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))

    user: Mapped["User"] = relationship("User", back_populates="transactions")
    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="transactions")
    security: Mapped["Security"] = relationship("Security", back_populates="transactions")



