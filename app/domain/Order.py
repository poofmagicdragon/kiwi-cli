

class PurchaseOrder():
    def __init__(self, portfolio_id:int, ticker: str, quantity: int):
        self.id = id
        self.portfolio_id = portfolio_id
        self.ticker = ticker
        self.quantity = quantity
        self.user = None
        


class SellOrder():
    def __init__(self, portfolio_id:int, ticker: str, quantity: int, sell_price: float):
        self.id = id
        self.portfolio_id = portfolio_id
        self.ticker = ticker
        self.quantity = quantity
        self.sell_price = sell_price
        self.user = None