from typing import Any


class StocksEndpoints:
    @staticmethod
    def get() -> list[str]:
        return []

    @staticmethod
    def post(data: dict[str, Any]) -> list[str]:
        return []

    @staticmethod
    def delete(index: str) -> None:
        return None
