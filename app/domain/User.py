from database import Base
from sqlalchemy import Column, String, Float

class User(Base):
    __tablename__ = 'USER'
    username = Column(String(30), primary_key=True)
    password = Column(String(30), nullable=False)
    firstname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    balance = Column(Float, nullable=False)

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