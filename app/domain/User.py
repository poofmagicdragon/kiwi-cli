from typing import List
# from app.domain import Portfolio
# from app.domain import Transaction
from app.database import Base
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship, mapped_column, Mapped


class User(Base):
    __tablename__ = 'user'
    username: Mapped[str] = mapped_column(String(30), primary_key = True)
    password: Mapped[str] = mapped_column(String(100), nullable = False)
    firstname: Mapped[str] = mapped_column(String(50), nullable = False)
    lastname: Mapped[str] = mapped_column(String(50), nullable = False)
    balance: Mapped[float] = mapped_column(Float, nullable = False)
    
    portfolios: Mapped[List["Portfolio"]] = relationship("Portfolio", back_populates="user")
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="user")

    # def __init__(self, username: str, password: str, firstname: str, lastname: str, balance: float):
    #     self.username = username
    #     self.password = password
    #     self.firstname = firstname
    #     self.lastname = lastname
    #     self.balance = balance
    
    # def __str__(self):
    #     return f"<User: username={self.username}; name={self.lastname}, {self.firstname}; balance={self.balance}>"


    def __str__(self):
        return(
            f"User(username='{self.username}', "
            f"firstname='{self.firstname} {self.lastname}', "
            f"balance={self.balance})"
        )