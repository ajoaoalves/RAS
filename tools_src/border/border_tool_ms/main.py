import logging

from .config import PICTURAS_LOG_LEVEL
from .core.message_processor import MessageProcessor
from .core.message_queue_setup import message_queue_connect
from .border_request_message import BorderRequestMessage
from .border_result_message import BorderResultMessage
from .border_tool import BorderTool

# Logging setup
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=PICTURAS_LOG_LEVEL, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    connection, channel = message_queue_connect()

    tool = BorderTool()
    request_msg_class = BorderRequestMessage
    result_msg_class = BorderResultMessage

    message_processor = MessageProcessor(tool, request_msg_class, result_msg_class, channel)

    try:
        message_processor.start()
    except KeyboardInterrupt:
        message_processor.stop()
        
    connection.close()