class Stock:
    name: str
    ticker: str
    price: float

    def __init__(
        self,
        name: str,
        ticker: str,
        price: float,
    ) -> None:
        self.name = name
        self.ticker = ticker
        self.price = price
