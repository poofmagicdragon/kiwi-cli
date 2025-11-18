
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
import pytest
from app.domain.security import Security
from app.service.security_service import get_all_securities, print_all_securities, get_price_by_ticker

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

def test_get_all_securities(db_session):
    test_security = Security(ticker="AAPL", issuer="Apple Inc.", price=150.0)
    test_security2 = Security(ticker="GOOGL", issuer="Alphabet Inc.", price=2800.0)
    db_session.add_all([test_security, test_security2])

    result = get_all_securities(db_session)

    assert len(result) == 2
    assert result[0].ticker == "AAPL"
    assert result[1].ticker == "GOOGL"

def test_print_all_securities(capsys, db_session):
    test_security = Security(ticker="AAPL", issuer="Apple Inc.", price=150.0)
    test_security2 = Security(ticker="GOOGL", issuer="Alphabet Inc.", price=2800.0)
    db_session.add_all([test_security, test_security2])

    securities = db_session.query(Security).all()
    print_all_securities(securities)

    captured = capsys.readouterr()
    output = captured.out

    assert "AAPL" in output
    assert "Apple Inc." in output
    assert "150.0" in output
    assert "GOOGL" in output
    assert "Alphabet Inc." in output
    assert "2800.0" in output

def test_get_price_by_ticker(db_session):
    test_security = Security(ticker="AAPL", issuer="Apple Inc.", price=150.0)
    db_session.add(test_security)

    price = get_price_by_ticker("AAPL", db_session)
    assert price == 150.0

    with pytest.raises(ValueError) as exc_info:
        get_price_by_ticker("MSFT", db_session)
    assert "Missing price for ticker 'MSFT'" in str(exc_info.value)




