from typing import Any

from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.collection import Collection

from core.stocks import StocksEndpoints

# # TODO(kba): move logger to config file
# logger = logging.getLogger()
# logger.setLevel("INFO")
# handler = logging.StreamHandler()
# formatter = logging.Formatter("%(asctime)s -- %(levelname)s -- %(message)s")
# handler.setFormatter(formatter)
# logger.addHandler(handler)


# class ProjectException(Exception):
#     pass

#     # Logs
#     @app.after_request
#     def after_request(response: Response) -> Response:
#         if response.status_code >= 200 and response.status_code < 300:
#             logger.info("%s %s %s", request.method, request.path, response.status)
#         else:
#             logger.error("%s %s %s", request.method, request.path, response.status)
#         return response

#     return app


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


def connect_mongodb() -> MongoCl:
    mongo = MongoCl()
    return mongo


def format_mongodb_reponse(data: list[Any]) -> list[Any]:
    output = []

    for document in data:
        document["id"] = str(document.pop("_id"))
        output.append(document)

    return output


def create_server(mongo: MongoCl, test_config=None) -> FastAPI:
    # Create an instance of FastAPI
    app = FastAPI()

    ##################
    # Define endpoints
    @app.get("/ready")
    def ready() -> str:
        return "ready"

    # Define the GET endpoint
    @app.get("/")
    def get_root() -> dict[str, Any]:
        # Read data from MongoDB collection
        stocks: list[Any] = mongo.col_stocks.find()  # type:ignore
        return {
            "stocks": format_mongodb_reponse(stocks),
        }

    @app.get("/stocks")
    def get_stocks() -> list[str]:
        return StocksEndpoints.get()

    @app.post("/stocks", status_code=201)
    def post_stocks() -> dict[str, Any]:
        # Parse input
        # parsed_body = request.json
        parsed_body = {}

        # Store data
        StocksEndpoints.post(parsed_body)
        return {}

    @app.delete("/stocks", status_code=204)
    def delete_stocks() -> None:
        raise NotImplementedError()

    return app
