from typing import Any

from fastapi import FastAPI

from core.stocks import StocksEndpoints, MongoCl
from core.dataclasses import Stock

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


def connect_mongodb() -> MongoCl:
    return MongoCl()


def create_server(mongodb: MongoCl, test_config=None) -> FastAPI:
    # Create an instance of FastAPI
    app = FastAPI()
    stocks_endpoints = StocksEndpoints(mongodb)

    ##################
    # Define endpoints
    @app.get("/ready")
    def ready() -> str:
        return "ready"

    # Define the GET endpoint
    @app.get("/")
    def get_root() -> dict[str, Any]:
        return {"message": "Hello world!"}

    @app.get("/stocks")
    def get_stocks() -> list[dict[str, Any]]:
        return stocks_endpoints.get()

    @app.post("/stocks", status_code=201)
    def post_stocks(stock: Stock) -> dict[str, Any]:
        # Store data
        stocks_endpoints.post(stock.model_dump())
        return {}

    @app.delete("/stocks", status_code=204)
    def delete_stocks(name: str) -> None:
        stocks_endpoints.delete(name)

    return app
