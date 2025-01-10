import json
import logging
import os
import random
import time
import uuid
from datetime import datetime

import pika
from pika.exchange_type import ExchangeType

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
PICTURAS_SRC_FOLDER = os.getenv("PICTURAS_SRC_FOLDER", "./images/src/")
PICTURAS_OUT_FOLDER = os.getenv("PICTURAS_OUT_FOLDER", "./images/out/")

LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)


def message_queue_connect():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()
    return connection, channel

def publish_request_message(channel, routing_key, request_id, procedure, parameters):
    # Build the request message payload
    message = {
        "messageId": request_id,
        "timestamp": datetime.now().isoformat(),
        "procedure": procedure,
        "parameters": parameters,
    }

    # Publish the message to the exchange
    channel.basic_publish(
        exchange="picturas.tools",
        routing_key=routing_key,  # Use key configured to route to the watermark tool queue (test purposes)
        body=json.dumps(message),
    )

    logging.info("Published request '%s' to '%s'", request_id, routing_key)


def publish_mock_requests_forever():
    try:
        while True:
            for file_name in os.listdir(PICTURAS_SRC_FOLDER):
                request_id = str(uuid.uuid4())

                watermark_parameters = {
                    "inputImageURI": os.path.join(PICTURAS_SRC_FOLDER, file_name),
                    "outputImageURI": os.path.join(PICTURAS_OUT_FOLDER, file_name)
                }

                publish_request_message(channel, "requests.watermark", request_id, "watermark", watermark_parameters)
                time.sleep(random.uniform(2, 5))
    finally:
        connection.close()


if __name__ == "__main__":
    connection, channel = message_queue_connect()
    publish_mock_requests_forever()
    # TODO receive and process result messages on separate thread / runtime
