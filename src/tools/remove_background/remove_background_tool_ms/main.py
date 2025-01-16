import logging

from .config import PICTURAS_LOG_LEVEL
from .core.message_processor import MessageProcessor
from .core.message_queue_setup import message_queue_connect
from .remove_background_request_message import RemoveBackgroundRequestMessage
from .remove_background_result_message import RemoveBackgroundResultMessage
from .remove_background_tool import RemoveBackgroundTool

# Logging setup
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=PICTURAS_LOG_LEVEL, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    # Set up the message queue connection
    connection, channel = message_queue_connect()

    # Initialize the tool, request, and result message classes
    tool = RemoveBackgroundTool()
    request_msg_class = RemoveBackgroundRequestMessage
    result_msg_class = RemoveBackgroundResultMessage

    # Create the message processor
    message_processor = MessageProcessor(tool, request_msg_class, result_msg_class, channel)

    try:
        LOGGER.info("Starting the RemoveBackgroundTool message processor...")
        message_processor.start()
    except KeyboardInterrupt:
        LOGGER.info("Stopping the RemoveBackgroundTool message processor...")
        message_processor.stop()
    finally:
        # Close the connection
        connection.close()
        LOGGER.info("Message queue connection closed.")
