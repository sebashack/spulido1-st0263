import pika

credentials = pika.PlainCredentials('admin', 'secret')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', port=5672, credentials=credentials))
channel = connection.channel()

print("Setting up file-service queue ...")

# Proucer
channel.exchange_declare('fs-producer', durable=True, exchange_type='direct')
channel.queue_declare(queue='fs-producer')
channel.queue_bind(exchange='fs-producer', queue='fs-producer', routing_key='msg-send')

# Consumer
channel.exchange_declare('fs-consumer', durable=True, exchange_type='direct')
channel.queue_declare(queue='fs-consumer')
channel.queue_bind(exchange='fs-consumer', queue='fs-consumer', routing_key='msg-receive')

channel.close()

print("Set up done!")
