import pika
from pika.exchange_type import ExchangeType
from rabbit_config import *

connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))
channel = connection.channel()


channel.exchange_declare(
        exchange=PICTURAS_EXCHANGE,
        exchange_type=ExchangeType.direct,
        durable=True,
    )

for queue in QUEUES:
    channel.queue_declare(queue=queue["name"], durable=queue["durable"])
    channel.queue_bind(exchange=PICTURAS_EXCHANGE, queue=queue["name"], routing_key=queue["routing_key"])

print("Queues for all tools have been set up successfully.")

print("Queue and exchange set up successfully.")
connection.close()
