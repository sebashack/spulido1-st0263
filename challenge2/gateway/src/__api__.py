import pika
from flask import Flask, request
from threading import Thread, Lock
import json

import files_grpc
import files_mom

# Mutex to switch between gRPC and MoM modes
mode_mutex = Lock()
app = Flask(__name__)


@app.route("/files/list", methods=["GET"])
def list_files():
    args = request.args

    limit = None
    try:
        limit = int(args["limit"])
    except:
        limit = None

    result = None
    mode_mutex.acquire()
    if app.config["IS_GRPC"]:
        app.config["IS_GRPC"] = False
        mode_mutex.release()
        result = files_grpc.list(app.config["GRPC_ADDR"], limit=limit)
        result["provider"] = "grpc"
    else:
        app.config["IS_GRPC"] = True
        mode_mutex.release()
        result = files_mom.list(app.config["MOM_CONNECTION"], limit=limit)
        result["provider"] = "mom"

    return result, result["status"]


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

    result = None
    mode_mutex.acquire()
    if app.config["IS_GRPC"]:
        app.config["IS_GRPC"] = False
        mode_mutex.release()
        result = files_grpc.search(
            app.config["GRPC_ADDR"], args["pattern"], limit=limit
        )
        result["provider"] = "grpc"
    else:
        app.config["IS_GRPC"] = True
        mode_mutex.release()
        result = files_mom.search(
            app.config["MOM_CONNECTION"], args["pattern"], limit=limit
        )
        result["provider"] = "mom"

    return result, result["status"]


def main():
    # gRPC setup
    app.config["GRPC_ADDR"] = "127.0.0.1:50051"

    # MoM setup
    credentials = pika.PlainCredentials("admin", "secret")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="127.0.0.1", port=5672, credentials=credentials)
    )

    app.config["MOM_CONNECTION"] = connection
    app.config["IS_GRPC"] = True

    app.run(debug=False, host="127.0.0.1", port=8001)


if __name__ == "__main__":
    main()
