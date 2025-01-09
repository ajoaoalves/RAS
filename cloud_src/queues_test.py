import pika
from rabbitmq.rabbit_config import *

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()

# Publish test messages to each queue
for queue in QUEUES:
    message = f"Test message for {queue['name']}"
    channel.basic_publish(
        exchange=PICTURAS_EXCHANGE,  # Default exchange
        routing_key=queue['routing_key'],  # Queue name as routing key
        body=message
    )
    print(f" [x] Sent '{message}' to queue '{queue}'")

# Close the connection
connection.close()
print("All test messages have been sent successfully.")
