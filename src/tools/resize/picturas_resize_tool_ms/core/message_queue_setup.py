import logging

import pika
from pika.adapters.blocking_connection import BlockingChannel

from ..config import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_PORT, RABBITMQ_USER

LOGGER = logging.getLogger(__name__)


def message_queue_connect() -> tuple[pika.BlockingConnection, BlockingChannel]:
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS),
        heartbeat=5,
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    return connection, channel
