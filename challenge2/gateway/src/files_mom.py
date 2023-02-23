import pika
import json


def list(conn, limit=None):
    message = {"type": "list", "limit": limit}
    channel = conn.channel()
    channel.basic_publish(
        exchange="fs-producer", routing_key="msg-send", body=json.dumps(message)
    )
    channel.close()


def search(conn, pattern, limit=None):
    message = {"type": "search", "pattern": pattern, "limit": limit}
    channel = conn.channel()
    channel.basic_publish(
        exchange="fs-producer", routing_key="msg-send", body=json.dumps(message)
    )
    channel.close()
