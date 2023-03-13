import json
import pika
import uuid


def list(app, limit=None):
    req_id = str(uuid.uuid4())
    message = {"type": "list", "limit": limit, "req_id": req_id}
    channel = mk_channel(app)
    channel.basic_publish(
        exchange="fs-producer", routing_key="msg-send", body=json.dumps(message)
    )
    channel.close()

    return consume_mom_queue(app, req_id)


def search(app, pattern, limit=None):
    req_id = str(uuid.uuid4())
    message = {"type": "search", "pattern": pattern, "limit": limit, "req_id": req_id}
    channel = mk_channel(app)
    channel.basic_publish(
        exchange="fs-producer", routing_key="msg-send", body=json.dumps(message)
    )
    channel.close()

    return consume_mom_queue(app, req_id)


# Helpers
def consume_mom_queue(app, correlation_id):
    result = {"error": "Failed to receive response", "status": 500}
    container = {"value": result}

    def on_response(channel, method, props, body):
        try:
            msg = json.loads(body)

            if msg["req_id"] == correlation_id:
                container["value"] = msg
                print(f"Message with key '{method.routing_key}'")
                container["value"]["status"] = 200

                channel.basic_cancel(consumer_tag=correlation_id)
                channel.close()
            else:
                print(f"Request-id mismatch: Discarding ...")
        except (JSONDecodeError, json.JSONDecodeError):
            pass

    # Consume the producer queue
    channel = mk_channel(app)
    channel.basic_consume(
        consumer_tag=correlation_id,
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
