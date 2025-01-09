
# RabbitMQ connection details
HOST = "localhost"

# Exchange details
PICTURAS_EXCHANGE= "picturas.tools"
EXCHANGE_DURABLE = True

# Queues and Routing keys
QUEUES = [
    {"name": "border_tool", "routing_key": "border", "durable": True},
    {"name": "crop_tool", "routing_key": "crop", "durable": True},
    {"name": "rotation_tool", "routing_key": "rotation", "durable": True},
    {"name": "brightness_tool", "routing_key": "brightness", "durable": True},
    {"name": "binarization_tool", "routing_key": "binarization", "durable": True},
    {"name": "resize_tool", "routing_key": "resize", "durable": True},
    {"name": "count_people_tool", "routing_key": "count_people", "durable": True},
    {"name": "object_detection_tool", "routing_key": "object_detection", "durable": True},
    {"name": "background_removal_tool", "routing_key": "background_removal", "durable": True},
    {"name": "watermark-requests", "routing_key": "requests.watermark", "durable": True},
    {"name": "results", "routing_key": "results", "durable": True},
]
