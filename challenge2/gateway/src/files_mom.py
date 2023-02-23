import json
import pika
import uuid


def list(conn, limit=None):
    message = {"type": "list", "limit": limit}
    channel = conn.channel()
    channel.basic_publish(
        exchange="fs-producer", routing_key="msg-send", body=json.dumps(message)
    )
    channel.close()

    return consume_mom_queue(conn)


def search(conn, pattern, limit=None):
    message = {"type": "search", "pattern": pattern, "limit": limit}
    channel = conn.channel()
    channel.basic_publish(
        exchange="fs-producer", routing_key="msg-send", body=json.dumps(message)
    )
    channel.close()

    return consume_mom_queue(conn)


# Helper
def consume_mom_queue(conn):
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

    # Consume the producer queue
    channel = conn.channel()
    channel.basic_consume(
        consumer_tag=tag,
        queue="fs-consumer",
        auto_ack=True,
        on_message_callback=on_response,
    )
    channel.start_consuming()

    return container["value"]
