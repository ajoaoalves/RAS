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

# tools_and_routing_keys = [
#     ("border_tool", "border"),
#     ("crop_tool", "crop"),
#     ("rotation_tool", "rotation"),
#     ("brightness_tool", "brightness"),
#     ("binarization_tool", "binarization"),
#     ("resize_tool", "resize"),
#     ("count_people_tool", "count_people"),
#     ("object_detection_tool", "object_detection"),
#     ("background_removal_tool", "background_removal"),
#     ("watermark-requests", "requests.watermark"),
#     ("results", "results"),
# ]


# for queue, routing_key in tools_and_routing_keys:
#     channel.queue_declare(queue=queue, durable=True)  # Declare the queue
#     channel.queue_bind(exchange='picturas.tools', queue=queue, routing_key=routing_key)  # Bind the queue to the exchange

for queue in QUEUES:
    channel.queue_declare(queue=queue["name"], durable=queue["durable"])
    channel.queue_bind(exchange=PICTURAS_EXCHANGE, queue=queue["name"], routing_key=queue["routing_key"])

print("Queues for all tools have been set up successfully.")

print("Queue and exchange set up successfully.")
connection.close()
