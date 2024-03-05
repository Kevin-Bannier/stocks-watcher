from pydantic import BaseModel
from typing import Optional


class Stock(BaseModel):
    # Mandatory params
    name: str
    ticker: str
    bourso_address: str

    # Optional params
    price: Optional[float] = None
