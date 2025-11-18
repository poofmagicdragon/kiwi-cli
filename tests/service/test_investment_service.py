from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
import pytest
from app.domain import Investment, Portfolio, User, Security
from app.service.investment_service import check_user_enough_balance, create_purchase_order, portfolio_has_sufficient_quantity, harvest_investment


# this runs before each test function
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    TestSessionLocal = sessionmaker(bind=engine)
    session = TestSessionLocal()
    yield session
    session.rollback()
    session.close()

def test_check_user_enough_balance(db_session):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=2000.0)
    db_session.add(test_user)

    test_security = Security(ticker ="AAPL", issuer="Apple Inc.", price = 150.0)
    db_session.add(test_security)

    result = check_user_enough_balance("AAPL", 4, db_session, test_user)
    result2 = check_user_enough_balance("AAPL", 20, db_session, test_user)
    assert result == True
    assert result2 == False

def test_create_purchase_order(db_session, monkeypatch):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=2000.0)
    test_portfolio = Portfolio(owner = "X", name = "Test Portfolio", description = "A test portfolio", investment_strategy = "Growth")
    test_security = Security(ticker ="AAPL", issuer="Apple Inc.", price = 150.0)
    db_session.add(test_security)
    db_session.add(test_user)
    db_session.add(test_portfolio)
    db_session.commit()

    inputs = iter([str(test_portfolio.id), "AAPL", "5"])
    monkeypatch.setattr("app.service.investment_service.get_all_portfolio_logged_in_user", lambda session: [test_portfolio])
    monkeypatch.setattr("app.service.investment_service._console.input", lambda _: next(inputs))

    create_purchase_order(db_session, test_user)

    investment = db_session.query(Investment).filter_by(ticker = "AAPL").all()
    assert investment[0].portfolio_id == 1
    assert investment[0].ticker == "AAPL"
    assert investment[0].quantity == 5
    assert test_user.balance == 1250.0 
    assert db_session.query(Investment).count() == 1

def test_create_purchase_order_no_portfolio(monkeypatch, db_session):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=2000.0)
    test_portfolio = Portfolio(owner = "X", name = "Test Portfolio", description = "A test portfolio", investment_strategy = "Growth")
    test_security = Security(ticker ="AAPL", issuer="Apple Inc.", price = 150.0)
    db_session.add(test_security)
    db_session.add(test_user)
    db_session.add(test_portfolio)
    db_session.commit()

    # portfolio id which does not exist
    inputs = iter(["5", "AAPL", "5"])
    monkeypatch.setattr("app.service.investment_service.get_all_portfolio_logged_in_user", lambda session: [test_portfolio])
    monkeypatch.setattr("app.service.investment_service._console.input", lambda _: next(inputs))

    result = create_purchase_order(db_session, test_user)
    assert result == "Portfolio ID 5 does not exist.  Please enter a valid portfolio ID"

def test_create_purchase_order_already_has_investment(monkeypatch, db_session):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=2000.0)
    test_portfolio = Portfolio(owner = "X", name = "Test Portfolio", description = "A test portfolio", investment_strategy = "Growth")
    test_security = Security(ticker ="AAPL", issuer="Apple Inc.", price = 150.0)
    test_investment = Investment(portfolio_id = 1, ticker = "AAPL", quantity = 1)
    db_session.add(test_security)
    db_session.add(test_user)
    db_session.add(test_portfolio)
    db_session.add(test_investment)
    db_session.commit()

    inputs = iter([str(test_portfolio.id), "AAPL", "5"])
    monkeypatch.setattr("app.service.investment_service.get_all_portfolio_logged_in_user", lambda session: [test_portfolio])
    monkeypatch.setattr("app.service.investment_service._console.input", lambda _: next(inputs))

    create_purchase_order(db_session, test_user)
    investment = db_session.query(Investment).filter_by(ticker = "AAPL").all()
    assert investment[0].portfolio_id == 1
    assert investment[0].ticker == "AAPL"
    assert investment[0].quantity == 6
    assert test_user.balance == 1250.0 
    assert db_session.query(Investment).count() == 1



def test_create_purchase_order_insufficient_balance(monkeypatch, db_session):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=200)
    test_portfolio = Portfolio(owner = "X", name = "Test Portfolio", description = "A test portfolio", investment_strategy = "Growth")
    test_security = Security(ticker ="AAPL", issuer="Apple Inc.", price = 150.0)
    db_session.add(test_security)
    db_session.add(test_user)
    db_session.add(test_portfolio)
    db_session.commit()

    # portfolio id which does not exist
    inputs = iter([str(test_portfolio.id), "AAPL", "5"])
    monkeypatch.setattr("app.service.investment_service.get_all_portfolio_logged_in_user", lambda session: [test_portfolio])
    monkeypatch.setattr("app.service.investment_service._console.input", lambda _: next(inputs))

    result = create_purchase_order(db_session, test_user)
    assert result == "Insufficient balance to make purchase"


def test_portfolio_has_sufficient_quantity(db_session):
    portfolio = Portfolio(owner="X", name="Test Portfolio", description="A test portfolio", investment_strategy="Growth")
    investment1 = Investment(portfolio_id=1, ticker="AAPL", quantity=10)
    investment2 = Investment(portfolio_id=1, ticker="MSFT", quantity=5)
    db_session.add(portfolio)
    db_session.add(investment1)
    db_session.add(investment2)
    db_session.commit()

    result = portfolio_has_sufficient_quantity(portfolio, "AAPL", 5, db_session)
    result2 = portfolio_has_sufficient_quantity(portfolio, "AAPL", 15, db_session)
    result3 = portfolio_has_sufficient_quantity(portfolio, "MSFT", 1, db_session)

    assert result == True
    assert result2 == False
    assert result3 == True

def test_harvest_investment(db_session, monkeypatch):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=1000.0)
    test_portfolio = Portfolio(owner = "X", name = "Test Portfolio", description = "A test portfolio", investment_strategy = "Growth")
    test_security = Security(ticker ="AAPL", issuer="Apple Inc.", price = 150.0)
    test_investment = Investment(portfolio_id=1, ticker="AAPL", quantity=10)
    db_session.add(test_security)
    db_session.add(test_user)
    db_session.add(test_portfolio)
    db_session.add(test_investment)
    db_session.commit()

    inputs = iter([str(test_portfolio.id), "AAPL", "5", "200"])
    monkeypatch.setattr("app.service.investment_service.get_all_portfolio_logged_in_user", lambda session: [test_portfolio])
    monkeypatch.setattr("app.service.investment_service._console.input", lambda _: next(inputs))

    harvest_investment(db_session, test_user)

    investment = db_session.query(Investment).filter_by(ticker = "AAPL").all()
    assert investment[0].quantity == 5
    assert test_user.balance == 2000
    assert db_session.query(Investment).count() == 1

def test_harvest_investment_no_portfolio(db_session, monkeypatch):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=1000.0)
    test_portfolio = Portfolio(owner = "X", name = "Test Portfolio", description = "A test portfolio", investment_strategy = "Growth")
    test_security = Security(ticker ="AAPL", issuer="Apple Inc.", price = 150.0)
    test_investment = Investment(portfolio_id=1, ticker="AAPL", quantity=10)
    db_session.add(test_security)
    db_session.add(test_user)
    db_session.add(test_portfolio)
    db_session.add(test_investment)
    db_session.commit()

    inputs = iter(["5", "AAPL", "5", "200"])
    monkeypatch.setattr("app.service.investment_service.get_all_portfolio_logged_in_user", lambda session: [test_portfolio])
    monkeypatch.setattr("app.service.investment_service._console.input", lambda _: next(inputs))

    result = harvest_investment(db_session, test_user)
    assert result == "Portfolio ID 5 does not exist.  Please enter a valid portfolio ID"

def test_harvest_investment_no_investment(db_session, monkeypatch):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=1000.0)
    test_portfolio = Portfolio(owner = "X", name = "Test Portfolio", description = "A test portfolio", investment_strategy = "Growth")
    test_security = Security(ticker ="AAPL", issuer="Apple Inc.", price = 150.0)
    test_investment = Investment(portfolio_id=1, ticker="AAPL", quantity=10)
    db_session.add(test_security)
    db_session.add(test_user)
    db_session.add(test_portfolio)
    db_session.add(test_investment)
    db_session.commit()

    inputs = iter([str(test_portfolio.id), "MSFT", "5", "200"])
    monkeypatch.setattr("app.service.investment_service.get_all_portfolio_logged_in_user", lambda session: [test_portfolio])
    monkeypatch.setattr("app.service.investment_service._console.input", lambda _: next(inputs))

    result = harvest_investment(db_session, test_user)
    assert result == "Portfolio 1 does not have any shares of MSFT"

def test_harvest_investment_id_nan(db_session, monkeypatch):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=1000.0)
    test_portfolio = Portfolio(owner = "X", name = "Test Portfolio", description = "A test portfolio", investment_strategy = "Growth")
    test_security = Security(ticker ="AAPL", issuer="Apple Inc.", price = 150.0)
    test_investment = Investment(portfolio_id=1, ticker="AAPL", quantity=10)
    db_session.add(test_security)
    db_session.add(test_user)
    db_session.add(test_portfolio)
    db_session.add(test_investment)
    db_session.commit()

    inputs = iter(["a", "AAPL", "5", "200"])
    monkeypatch.setattr("app.service.investment_service.get_all_portfolio_logged_in_user", lambda session: [test_portfolio])
    monkeypatch.setattr("app.service.investment_service._console.input", lambda _: next(inputs))
    
    result = harvest_investment(db_session, test_user)

    assert result == "Invalid input: 'a' is not a number"

def test_harvest_investment_not_enough_shares(db_session, monkeypatch):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=1000.0)
    test_portfolio = Portfolio(owner = "X", name = "Test Portfolio", description = "A test portfolio", investment_strategy = "Growth")
    test_security = Security(ticker ="AAPL", issuer="Apple Inc.", price = 150.0)
    test_investment = Investment(portfolio_id=1, ticker="AAPL", quantity=10)
    db_session.add(test_security)
    db_session.add(test_user)
    db_session.add(test_portfolio)
    db_session.add(test_investment)
    db_session.commit()

    inputs = iter([str(test_portfolio.id), "AAPL", "15", "200"])
    monkeypatch.setattr("app.service.investment_service.get_all_portfolio_logged_in_user", lambda session: [test_portfolio])
    monkeypatch.setattr("app.service.investment_service._console.input", lambda _: next(inputs))
    
    result = harvest_investment(db_session, test_user)

    assert result == "Insufficient quantity to make sale"

