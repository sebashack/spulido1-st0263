import json
import pika
import uuid


def list(app, limit=None):
    message = {"type": "list", "limit": limit}
    channel = mk_channel(app)
    channel.basic_publish(
        exchange="fs-producer", routing_key="msg-send", body=json.dumps(message)
    )
    channel.close()

    return consume_mom_queue(app)


def search(app, pattern, limit=None):
    message = {"type": "search", "pattern": pattern, "limit": limit}
    channel = mk_channel(app)
    channel.basic_publish(
        exchange="fs-producer", routing_key="msg-send", body=json.dumps(message)
    )
    channel.close()

    return consume_mom_queue(app)


# Helpers
def consume_mom_queue(app):
    tag = str(uuid.uuid4())
    result = {"error": "Failed to receive response", "status": 500}
    container = {"value": result}

    def on_response(channel, method, props, body):
        try:
            container["value"] = json.loads(body)
            print(f"Message with key '{method.routing_key}'")
            container["value"]["status"] = 200
        finally:
            channel.basic_cancel(consumer_tag=tag)
            channel.close()

    # Consume the producer queue
    channel = mk_channel(app)
    channel.basic_consume(
        consumer_tag=tag,
        queue="fs-consumer",
        auto_ack=True,
        on_message_callback=on_response,
    )
    channel.start_consuming()

    return container["value"]


def mk_connection(credentials, host, port):
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    )


def mk_channel(app):
    channel = None
    try:
        channel = app.config["MOM_CONNECTION"].channel()
    except Exception as e:
        print(e)
        reconnect_if_closed(app)
        channel = app.config["MOM_CONNECTION"].channel()

    return channel


def reconnect_if_closed(app):
    if app.config["MOM_CONNECTION"].is_closed:
        info = app.config["MOM_CONN_INFO"]
        app.config["MOM_CONNECTION"] = mk_connection(
            info["credentials"], info["host"], info["port"]
        )
