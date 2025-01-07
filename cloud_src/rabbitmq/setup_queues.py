import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='image_exchange', exchange_type='direct')

# List of queues with their routing keys
tools_and_routing_keys = [
    ("border_tool", "border"),
    ("crop_tool", "crop"),
    ("rotation_tool", "rotation"),
    ("brightness_tool", "brightness"),
    ("binarization_tool", "binarization"),
    ("resize_tool", "resize"),
    ("count_people_tool", "count_people"),
    ("object_detection_tool", "object_detection"),
    ("background_removal_tool", "background_removal"),
    ("watermark_tool", "watermark"),
]

# Declare and bind each queue
for queue, routing_key in tools_and_routing_keys:
    channel.queue_declare(queue=queue, durable=True)  # Declare the queue
    channel.queue_bind(exchange='image_exchange', queue=queue, routing_key=routing_key)  # Bind the queue to the exchange


print("Queues for all tools have been set up successfully.")

print("Queue and exchange set up successfully.")
connection.close()
