import logging

from .config import PICTURAS_LOG_LEVEL
from .core.message_processor import MessageProcessor
from .core.message_queue_setup import message_queue_connect
from .crop_request_message import CropRequestMessage
from .crop_result_message import CropResultMessage
from .crop_tool import CropTool

# Logging setup
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level=PICTURAS_LOG_LEVEL, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    connection, channel = message_queue_connect()

    tool = CropTool()
    request_msg_class = CropRequestMessage
    result_msg_class = CropResultMessage

    message_processor = MessageProcessor(
        tool, request_msg_class, result_msg_class, channel
    )

    try:
        message_processor.start()
    except KeyboardInterrupt:
        message_processor.stop()

    connection.close()
