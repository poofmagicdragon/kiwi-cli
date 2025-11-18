from app.database import Base
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
# from app.domain import Portfolio, Security

class Investment(Base):
    __tablename__ = 'investment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    portfolio_id: Mapped[int] = mapped_column(ForeignKey("portfolio.id"), nullable=False)
    ticker: Mapped[str] = mapped_column(ForeignKey("security.ticker"), nullable=False)

    portfolio: Mapped["Portfolio"] = relationship("Portfolio", back_populates="investments")
    security: Mapped["Security"] = relationship("Security", back_populates="investments")
