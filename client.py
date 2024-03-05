from requests import Session
from argparse import ArgumentParser, _SubParsersAction


SERVER_HOST = "127.0.0.1"
SERVER_PORT = "8080"


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()

    action: _SubParsersAction = parser.add_subparsers(dest="action")
    action.add_parser("provision")
    action.add_parser("get")

    delete: ArgumentParser = action.add_parser("delete")
    delete.add_argument(
        "--name", type=str, required=True, help="Name of stock to delete"
    )

    return parser


def provision() -> None:
    items = [
        {"name": "air liquide", "ticker": "air", "bourso_address": "a"},
        {"name": "engie", "ticker": "engie", "bourso_address": "a"},
        {"name": "lvmh", "ticker": "lvmh", "bourso_address": "a"},
        {"name": "loreal", "ticker": "loreal", "bourso_address": "a"},
        {"name": "hermes", "ticker": "hermes", "bourso_address": "a"},
        {"name": "kering", "ticker": "kering", "bourso_address": "a"},
        {"name": "michelin", "ticker": "michelin", "bourso_address": "a"},
        {"name": "total", "ticker": "total", "bourso_address": "a"},
    ]

    session = Session()
    for item in items:
        resp = session.post(f"http://{SERVER_HOST}:{SERVER_PORT}/stocks", json=item)
        print("-", item["name"], resp.status_code)


def get_stocks() -> None:
    session = Session()
    resp = session.get(f"http://{SERVER_HOST}:{SERVER_PORT}/stocks")

    if resp.status_code == 200:
        print("Response:\n", resp.json())
    else:
        print("Response status", resp.status_code)
        print("Response content", resp.text)


def delete_stock(name: str) -> None:
    session = Session()
    resp = session.delete(f"http://{SERVER_HOST}:{SERVER_PORT}/stocks?name={name}")
    print("Response:", resp.status_code, resp.text)


def main() -> None:
    # Parse args
    parser = get_parser()
    args = parser.parse_args()

    if args.action == "get":
        get_stocks()
    elif args.action == "delete":
        delete_stock(args.name)
    elif args.action == "provision":
        provision()
    else:
        print("Do nothing")


if __name__ == "__main__":
    main()
