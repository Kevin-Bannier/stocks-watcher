from server import connect_mongodb, create_server
import uvicorn


def main():
    print("Connecting to MongoDB database...")
    mdb = connect_mongodb()

    print("Starting HTTP server...")
    app = create_server(mdb)
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
