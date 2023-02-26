import argparse
import json
import logging
import pathlib
import pika
import sys


def list_files(dir_path, pattern="*", limit=None):
    files = list(map(lambda p: str(p), pathlib.Path(dir_path).glob("**/" + pattern)))
    if limit is None or limit < 1:
        return {"found": len(files), "files": files}
    else:
        return {"found": len(files), "files": files[:limit]}


def on_request(logger, dir_path, conn, channel, method, props, body):
    result = None
    try:
        msg = json.loads(body)
        logger.info(f"Message with key '{method.routing_key} and type '{msg['type']}'")
        if msg["type"] == "search":
            result = list_files(dir_path, msg["pattern"], msg["limit"])
        else:
            result = list_files(dir_path, limit=msg["limit"])
        result["req_id"] = msg["req_id"]
    except Exception as e:
        print(e)
        logger.warning(f"Failed to process message")
        result = {"error": "Failed to process file request", "req_id": msg["req_id"]}

    channel.basic_publish(
        exchange="fs-consumer", routing_key="msg-receive", body=json.dumps(result)
    )


def main(argv):
    parser = argparse.ArgumentParser(description="File service API gateway")

    parser.add_argument("config", type=str, help="Path to config file")

    args = parser.parse_args(argv[1:])

    config_path = args.config
    conf = json.loads(open(config_path, "r").read())

    # MoM setup
    credentials = pika.PlainCredentials(conf["rabbit_user"], conf["rabbit_password"])
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=conf["rabbit_host"], port=conf["rabbit_port"], credentials=credentials
        )
    )

    # Logging
    FORMAT = "%(asctime)s -- %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger("mom-consumer-server")

    def cb(ch, method, props, body):
        on_request(logger, conf["dir_path"], connection, ch, method, props, body)

    # Consume the producer queue
    channel = connection.channel()
    channel.basic_consume(queue="fs-producer", auto_ack=True, on_message_callback=cb)
    channel.start_consuming()


if __name__ == "__main__":
    main(sys.argv)
