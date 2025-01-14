import functools
import logging
import time
from threading import Thread
from typing import Any, List, Type

from pika.adapters.blocking_connection import BlockingChannel
from pydantic import ValidationError

from ..config import (PICTURAS_MS_NAME, PICTURAS_NUM_THREADS, RABBITMQ_REQUESTS_QUEUE_NAME, RABBITMQ_RESULTS_EXCHANGE,
                      RABBITMQ_RESULTS_ROUTING_KEY)
from .messages.request_message import RequestMessage
from .messages.result_message import ResultMessage
from .tool import Tool

LOGGER = logging.getLogger(__name__)


class MessageProcessor:

    def __init__(
        self,
        tool: Tool,
        request_msg_class: Type[RequestMessage],
        result_msg_class: Type[ResultMessage],
        channel: BlockingChannel,
    ):
        self.threads: List[Thread] = []

        self.tool = tool
        self.request_msg_class = request_msg_class
        self.result_msg_class = result_msg_class

        self.channel = channel

        # This message processor spawns a thread for each incoming message.
        # Setting the 'prefetch_count' limits the number of messages that can be processed concurrently.
        # Note: In a production, experiment with different 'prefetch_count' values to optimize performance and resource utilization.
        self.channel.basic_qos(prefetch_count=int(PICTURAS_NUM_THREADS))

        self.channel.basic_consume(
            on_message_callback=functools.partial(self.on_request_message, args=self),
            queue=RABBITMQ_REQUESTS_QUEUE_NAME,
        )

    def ack_message(self, ch, delivery_tag):
        """
        Acknowledge that the message was processed.
        """
        if ch.is_open:
            ch.basic_ack(delivery_tag)
        else:
            LOGGER.warning("Trying to ACK message on a closed channel")

    def send_response_message(self, ch, request_msg: RequestMessage, tool_result: Any, exception: Exception | None,
                              processing_time: float):
        """
        Send a response message to the 'results'.
        """
        result_msg = self.result_msg_class(request_msg, tool_result, exception, processing_time, PICTURAS_MS_NAME)

        ch.basic_publish(
            exchange=RABBITMQ_RESULTS_EXCHANGE,
            routing_key=RABBITMQ_RESULTS_ROUTING_KEY,
            body=result_msg.model_dump_json(),
        )

        logging.info("Published result of '%s' to '%s'", result_msg.correlationId, RABBITMQ_RESULTS_ROUTING_KEY)

    def handle_request_message(self, ch, delivery_tag, body):
        """
        Handle a request message received from the queue.
        This function will parse the message, apply the tool, and send the response through the 'results' queue.
        """
        try:
            request_msg: RequestMessage = self.request_msg_class.model_validate_json(body)
            LOGGER.debug("Request parsed: %s", request_msg)

            tool_result: Any = None
            exception: Exception | None = None
            start_ts = time.time()

            try:
                tool_result = self.tool.apply(request_msg.parameters)
            except Exception as e:
                exception = e
                LOGGER.error("Error: %s", e)

            time_elapsed = time.time() - start_ts

            LOGGER.info("Processed request '%s' (took %.3f s)", request_msg.messageId, time_elapsed)

            ch.connection.add_callback_threadsafe(
                functools.partial(self.send_response_message, ch, request_msg, tool_result, exception, time_elapsed))
        except ValidationError as e:
            LOGGER.error("Validation error: %s", e)

        ch.connection.add_callback_threadsafe(functools.partial(self.ack_message, ch, delivery_tag))

    def on_request_message(self, ch, method_frame, _header_frame, body, args):
        delivery_tag = method_frame.delivery_tag
        t = Thread(target=self.handle_request_message, args=(ch, delivery_tag, body))
        t.start()
        self.threads.append(t)

    def start(self) -> None:
        self.channel.start_consuming()

    def stop(self) -> None:
        self.channel.stop_consuming()

        # Wait for all threads to complete
        for thread in self.threads:
            thread.join()

        self.threads = []
