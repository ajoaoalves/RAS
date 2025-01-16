import json
import logging
import os
import random
import time
import uuid
import sys
from datetime import datetime

import pika
from pika.exchange_type import ExchangeType

from rabbitmq.rabbit_config import *

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


def message_queue_setup(channel,procedure_name):
    channel.exchange_declare(
        exchange="picturas.tools",
        exchange_type=ExchangeType.direct,
        durable=True,
    )
    channel.queue_declare(queue="results", durable=True)
    channel.queue_bind(
        queue="results",
        exchange="picturas.tools",
        routing_key="results",
    )
    
    channel.queue_declare(queue=f"{procedure_name}-requests", durable=True)
    channel.queue_bind(
        queue=f"{procedure_name}-requests",
        exchange="picturas.tools",
        routing_key=f"requests.{procedure_name}",
    )


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


def publish_mock_requests_forever(procedure_name):
    try:
        while True:

            for file_name in os.listdir(PICTURAS_SRC_FOLDER):
                request_id = str(uuid.uuid4())
                parameters = {
                    "inputImageURI": os.path.join(PICTURAS_SRC_FOLDER, file_name),
                    "outputImageURI": os.path.join(PICTURAS_OUT_FOLDER, file_name)
                }

                # Add additional parameters based on procedure name
                if procedure_name == "brightness":
                    parameters["brightnessValue"] = random.uniform(0, 2.0)

                elif procedure_name == "resize":
                    parameters["width"] = random.randint(100, 1920)
                    parameters["height"] = random.randint(100, 1080)

                elif procedure_name == "border":
                    bordersize = random.randint(1, 10)
                    bordercolor = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    parameters["bordersize"] = bordersize
                    parameters["bordercolor"] = bordercolor
                    
                elif procedure_name == "count-people":
                    parameters = {
                        "inputImageURI": os.path.join(PICTURAS_SRC_FOLDER, file_name)
                    }
                elif procedure_name == "object-detection":
                    parameters = {
                        "inputImageURI": os.path.join(PICTURAS_SRC_FOLDER, file_name)
                    }

                elif procedure_name == "crop":
                    # Define random crop box values
                    crop_left = random.randint(0, 100)
                    crop_upper = random.randint(0, 100)
                    crop_right = random.randint(crop_left + 50, crop_left + 200)
                    crop_lower = random.randint(crop_upper + 50, crop_upper + 200)

                    # Ensure crop box is valid and within bounds
                    crop_box = (crop_left, crop_upper, crop_right, crop_lower)
                    parameters = {
                        "crop_box": crop_box
                    }
                
                publish_request_message(channel, "requests." + procedure_name, request_id, procedure_name, parameters)
                time.sleep(random.uniform(2, 5))
    finally:
        connection.close()


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print('''
              Usage: python test_requests.py <procedure_name>
    
    Possible procedure_name:
            
            border
            crop
            rotation
            brightness
            binarization
            resize
            count-people
            object-detection
            background-removal
            watermark
            
              ''')
        sys.exit(1)

    procedure_name = sys.argv[1]  # The first argument is the procedure name

    connection, channel = message_queue_connect()
    message_queue_setup(channel,procedure_name)
    publish_mock_requests_forever(procedure_name)
    # TODO receive and process result messages on separate thread / runtime
