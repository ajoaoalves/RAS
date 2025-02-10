import logging

from .config import PICTURAS_LOG_LEVEL, PICTURAS_WATERMARK_IMAGE_PATH
from .core.message_processor import MessageProcessor
from .core.message_queue_setup import message_queue_connect
from .watermark_request_message import WatermarkRequestMessage
from .watermark_result_message import WatermarkResultMessage
from .watermark_tool import WatermarkTool

# Logging setup
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=PICTURAS_LOG_LEVEL, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    connection, channel = message_queue_connect()

    tool = WatermarkTool(PICTURAS_WATERMARK_IMAGE_PATH)
    request_msg_class = WatermarkRequestMessage
    result_msg_class = WatermarkResultMessage

    message_processor = MessageProcessor(tool, request_msg_class, result_msg_class, channel)

    try:
        message_processor.start()
    except KeyboardInterrupt:
        message_processor.stop()

    connection.close()
