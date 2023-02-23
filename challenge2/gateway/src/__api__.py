from flask import Flask, request
import json

import files_grpc

app = Flask(__name__)


@app.route("/files/list", methods=["GET"])
def list_files():
    args = request.args

    limit = None
    try:
        limit = int(args["limit"])
    except:
        limit = None

    result = files_grpc.list(app.config["GRPC_ADDR"], limit=limit)
    return json.loads(result)


@app.route("/files/search", methods=["GET"])
def search_files():
    args = request.args

    if "pattern" not in args:
        return {"error": "missing pattern"}, 400

    limit = None
    try:
        limit = int(args["limit"])
    except:
        limit = None

    result = files_grpc.search(app.config["GRPC_ADDR"], args["pattern"], limit=limit)
    return json.loads(result)


def main():
    app.config["GRPC_ADDR"] = "127.0.0.1:50051"
    app.run(debug=False, host="127.0.0.1", port=8001)


if __name__ == "__main__":
    main()
