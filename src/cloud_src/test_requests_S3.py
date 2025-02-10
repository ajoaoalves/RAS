import json
import logging
import os
import random
import time
import uuid
import sys
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

import pika
from pika.exchange_type import ExchangeType

from rabbitmq.rabbit_config import *

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
PICTURAS_SRC_FOLDER = os.getenv("PICTURAS_SRC_FOLDER", "./images/src/")
PICTURAS_OUT_FOLDER = os.getenv("PICTURAS_OUT_FOLDER", "./images/out/")
S3_SRC_FOLDER =  "src/"
S3_OUT_FOLDER =  "out/"

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


def publish_mock_requests_forever(procedure_name):
    try:
        while True:

            for file_name in os.listdir(PICTURAS_SRC_FOLDER):
                request_id = str(uuid.uuid4())
                parameters = {
                    "inputImageURI": os.path.join(S3_SRC_FOLDER, file_name),
                    "outputImageURI": os.path.join(S3_OUT_FOLDER, file_name)
                }

                # Add additional parameters based on procedure name
                if procedure_name == "brightness":
                    parameters["brightnessValue"] = random.uniform(0, 2.0)

                if procedure_name == "rotation":
                    parameters["angle"] = random.randint(0, 360)

                elif procedure_name == "resize":
                    parameters["width"] = random.randint(100, 1920)
                    parameters["height"] = random.randint(100, 1080)

                elif procedure_name == "border":
                    bordersize = random.randint(1, 10)
                    bordercolor = "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    parameters["bordersize"] = bordersize
                    parameters["bordercolor"] = bordercolor

                elif procedure_name == "crop":
                    # Define random crop box values
                    crop_left = random.randint(0, 100)
                    crop_upper = random.randint(0, 100)
                    crop_right = random.randint(crop_left + 50, crop_left + 200)
                    crop_lower = random.randint(crop_upper + 50, crop_upper + 200)

                    # Ensure crop box is valid and within bounds
                    crop_box = (crop_left, crop_upper, crop_right, crop_lower)
                    parameters["crop_box"] = crop_box
                    
                publish_request_message(channel, "requests." + procedure_name, request_id, procedure_name, parameters)
                # print(f"Published request for {procedure_name} with parameters: {parameters}")  # Log the published request
                time.sleep(random.uniform(1, 1))
    finally:
        connection.close()

# Function to check if a bucket exists
def bucket_exists(bucket_name):
    try:
        client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' exists.")
        return True
    except ClientError as e:
        # Check if the error is a 404 (bucket not found)
        if e.response['Error']['Code'] == '404':
            print(f"Bucket '{bucket_name}' does not exist.")
        else:
            print(f"Error occurred: {e}")
        return False


# Function to create a bucket
def create_bucket(bucket_name):
    try:
        client.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        print(f"Failed to create bucket '{bucket_name}': {e}")
        sys.exit(1)

# Function to upload files from local directory to MinIO bucket
def upload_files_to_bucket(bucket_name, local_src_path, s3_dest_path):
    for root, _, files in os.walk(local_src_path):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            s3_key = os.path.join(s3_dest_path, file_name)

            try:
                client.upload_file(local_file_path, bucket_name, s3_key)
                print(f"Uploaded '{local_file_path}' to '{bucket_name}/{s3_key}'.")
            except ClientError as e:
                print(f"Failed to upload '{local_file_path}': {e}")

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


    # Ensure S3 bucket 'images' exists
    client = boto3.client(
            's3',
            endpoint_url="http://localhost:9000",
            aws_access_key_id='ROOTNAME',
            aws_secret_access_key='CHANGEME123',
            region_name='us-east-1'
        )


    # Example usage
    bucket_name = "images"
    if bucket_exists(bucket_name):
        print(f"Proceeding with bucket '{bucket_name}'...")
    else:
        print(f"Bucket '{bucket_name}' does not exist. Creating it...")
        create_bucket(bucket_name)
    
    # Copy images from ./images/src/* to MinIO bucket
    local_src_folder = "./images/src"
    s3_dest_folder = "src"

    if os.path.exists(local_src_folder):
        upload_files_to_bucket(bucket_name, local_src_folder, s3_dest_folder)
    else:
        print(f"Local source folder '{local_src_folder}' does not exist. Exiting.")
        sys.exit(1)
    
    procedure_name = sys.argv[1]  # The first argument is the procedure name

    connection, channel = message_queue_connect()
    publish_mock_requests_forever(procedure_name)
    # TODO receive and process result messages on separate thread / runtime
