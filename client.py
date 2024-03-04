from requests import Session
from argparse import ArgumentParser, _SubParsersAction


SERVER_HOST = "127.0.0.1"
SERVER_PORT = "8080"


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()

    action: _SubParsersAction = parser.add_subparsers(dest="action")
    action.add_parser("provision")
    action.add_parser("get")

    return parser


def provision() -> None:
    items = [
        {"name": "air liquide", "price": 150.0},
        {"name": "total", "price": 50.0},
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


def main() -> None:
    # Parse args
    parser = get_parser()
    args = parser.parse_args()

    print(args.action)

    if args.action == "provision":
        provision()
    elif args.action == "get":
        get_stocks()
    else:
        print("Do nothing")


if __name__ == "__main__":
    main()
