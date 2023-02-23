from flask import Flask
import json

import files_grpc

app = Flask(__name__)


@app.route("/files/list")
def list_files():
    files = files_grpc.list(app.config["GRPC_ADDR"])
    return {"files": files}


@app.route("/files/search")
def search_files():
    files = files_grpc.search(app.config["GRPC_ADDR"])
    return {"files": files}


def main():
    app.config["GRPC_ADDR"] = "127.0.0.1:50051"
    app.run(debug=False, host="127.0.0.1", port=8001)


if __name__ == "__main__":
    main()
