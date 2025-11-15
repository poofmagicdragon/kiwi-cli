
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
import pytest
from app.domain import Portfolio, User
from app.service.portfolio_service import create_portfolio, get_all_portfolio_logged_in_user, get_portfolio_by_name, get_all_portfolios, print_all_portfolios, delete_portfolio
from app.service.user_service import get_logged_in_user, _logged_in_user

# # mock db setup here 
# test_engine = create_engine("sqlite:///:memory:", echo=False)
# Base.metadata.create_all(test_engine)
# TestSessionLocal = sessionmaker(bind = test_engine)


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

def test_create_portfolio(monkeypatch, db_session):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=100.1)
    db_session.add(test_user)
    db_session.commit()

    inputs = iter(["test", "sample desc", "sure"])
    monkeypatch.setattr("app.service.portfolio_service._console.input", lambda _: next(inputs))

    create_portfolio(db_session, test_user)
    portfolio = db_session.query(Portfolio).filter_by(owner = "X").one_or_none()

    assert portfolio is not None
    assert portfolio.name == "test"
    assert portfolio.description == "sample desc"
    assert portfolio.investment_strategy == "sure"

def test_get_portfolio_by_name(db_session):
    test_portfolio = Portfolio(owner="Y", name="portfolio y", description="desc", investment_strategy="growth")
    db_session.add(test_portfolio)

    portfolio = get_portfolio_by_name("portfolio y", db_session)

    assert portfolio is not None
    assert portfolio.name == "portfolio y"

def test_get_all_portfolios(db_session):
    test_portfolio = Portfolio(owner="X", name="test", description="sample desc", investment_strategy="sure1")
    test_portfolio2 = Portfolio(owner="jd", name="port 2", description="this is an description", investment_strategy="long term")
    db_session.add_all([test_portfolio, test_portfolio2])

    portfolios = get_all_portfolios(db_session)
    
    assert portfolios[0].name == "test"
    assert portfolios[1].name == "port 2"

def test_print_all_portfolios(capsys, db_session):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=100.1)
    test_portfolio = Portfolio(owner="X", name="test", description="sample desc", investment_strategy="sure1")
    test_portfolio2 = Portfolio(owner="X", name="port 2", description="this is an description", investment_strategy="long term")
    db_session.add(test_user)
    db_session.add_all([test_portfolio, test_portfolio2])

    print_all_portfolios(db_session)

    captured = capsys.readouterr()
    output = captured.out

    assert "test" in output
    assert "sample desc" in output
    assert "sure1" in output
    assert "port 2" in output
    assert "description" in output
    assert "long term" in output

def test_delete_portfolio(db_session):
    test_portfolio = Portfolio(owner="X", name="test", description="sample desc", investment_strategy="sure1")
    db_session.add(test_portfolio)

    input = "test"
    delete_portfolio(db_session, input)
    portfolio = db_session.query(Portfolio).filter_by(name = "test").one_or_none()

    assert portfolio is None

def test_get_all_portfolio_logged_in_user(monkeypatch, db_session):
    test_user = User(username="X", firstname="First", lastname="Last", password="Y", balance=100.1)
    test_portfolio = Portfolio(owner="X", name="test", description="sample desc", investment_strategy="sure1")
    test_portfolio2 = Portfolio(owner="X", name="port 2", description="this is an description", investment_strategy="long term")
    test_portfolio3 = Portfolio(owner="jd", name="port 3", description="desc 3", investment_strategy="strategy 3")
    db_session.add(test_user)
    db_session.add_all([test_portfolio, test_portfolio2, test_portfolio3])

    monkeypatch.setattr("app.service.user_service._logged_in_user", test_user)

    portfolios = get_all_portfolio_logged_in_user(db_session)

    assert len(portfolios) == 2
    assert portfolios[0].owner == "X"
    assert portfolios[1].owner == "X"


