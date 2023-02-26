from flask import Flask, request
from threading import Thread, Lock
import argparse
import json
import pika
import sys

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
        result = files_mom.list(app, limit=limit)
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
        result = files_mom.search(app, args["pattern"], limit=limit)
        result["provider"] = "mom"

    return result, result["status"]


def main(argv):
    parser = argparse.ArgumentParser(description="File service API gateway")

    parser.add_argument("config", type=str, help="Path to config file")

    args = parser.parse_args(argv[1:])

    config_path = args.config

    conf = json.loads(open(config_path, "r").read())

    # gRPC setup
    app.config["GRPC_ADDR"] = f"{conf['grpc_host']}:{conf['grpc_port']}"

    # MoM setup
    credentials = pika.PlainCredentials(conf['rabbit_user'], conf['rabbit_password'])
    app.config["MOM_CONNECTION"] = files_mom.mk_connection(
        credentials, conf['rabbit_host'], conf['rabbit_port']
    )
    app.config["MOM_CONN_INFO"] = {
        "host": conf['rabbit_host'],
        "port": conf['rabbit_port'],
        "credentials": credentials,
    }
    app.config["IS_GRPC"] = True

    app.run(debug=False, host=conf['host'], port=conf['port'])


if __name__ == "__main__":
    main(sys.argv)
