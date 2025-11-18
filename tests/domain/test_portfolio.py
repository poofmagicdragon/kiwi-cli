from app.domain.Portfolio import Portfolio, __str__

def test_portfolio_representation():
    portfolio = Portfolio(id  = 1, name="test portfolio", description="its a test", investment_strategy="grow", owner="test_user")

    result = portfolio.__str__()
    assert result == "<Portfolio(name=test portfolio, description=its a test, user=test_user)>"

