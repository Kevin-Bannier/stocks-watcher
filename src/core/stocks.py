from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection


MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017


class MongoCl:
    col_stocks: Collection

    def __init__(self) -> None:
        # MongoDB connection setup
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client["db_name"]

        self.provision_mongo()
        self.col_stocks = self.db["stocks"]

    def provision_mongo(self) -> None:
        collections = self.db.list_collection_names()
        if "stocks" not in collections:
            self.db.create_collection("stocks")
            items = [
                {"name": "air liquide", "price": 150.0},
                {"name": "total", "price": 50.0},
            ]
            self.db["stocks"].insert_many(items)


########
## Utils
def format_mongodb_reponse(data: list[Any]) -> list[Any]:
    output = []

    for document in data:
        document["id"] = str(document.pop("_id"))
        output.append(document)

    return output


class StocksEndpoints:
    mongodb: MongoCl

    def __init__(self, mongodb: MongoCl) -> None:
        self.mongodb = mongodb

    def get(self) -> list[dict[str, Any]]:
        # Read data from MongoDB collection
        stocks: list[dict[str, Any]] = self.mongodb.col_stocks.find()  # type:ignore

        return format_mongodb_reponse(stocks)

    def post(self, data: dict[str, Any]) -> dict[str, Any]:
        # Check data:
        if set(data.keys()) != {"name", "price"}:
            raise ValueError(f"Keys are incorrect: {','.join(data.keys())}")
        self.mongodb.db["stocks"].insert_one(data)
        return {}

    def delete(self, index: str) -> None:
        return None
