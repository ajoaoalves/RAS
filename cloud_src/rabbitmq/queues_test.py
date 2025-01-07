import pika

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'  # Update this to your RabbitMQ container's hostname or IP if not localhost
queues = [
    "border_tool",
    "crop_tool",
    "rotation_tool",
    "brightness_tool",
    "binarization_tool",
    "resize_tool",
    "count_people_tool",
    "object_detection_tool",
    "background_removal_tool",
    "watermark_tool",
]

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()

# Publish test messages to each queue
for queue in queues:
    message = f"Test message for {queue}"
    channel.basic_publish(
        exchange='',  # Default exchange
        routing_key=queue,  # Queue name as routing key
        body=message
    )
    print(f" [x] Sent '{message}' to queue '{queue}'")

# Close the connection
connection.close()
print("All test messages have been sent successfully.")
