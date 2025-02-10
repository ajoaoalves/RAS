import logging

from .config import PICTURAS_LOG_LEVEL, PICTURAS_YOLO_MODEL_PATH
from .core.message_processor import MessageProcessor
from .core.message_queue_setup import message_queue_connect
from .count_objects_request_message import CountObjectsRequestMessage
from .count_objects_result_message import CountObjectsResultMessage
from .count_objects_tool import CountObjects

# Configuração de logging
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=PICTURAS_LOG_LEVEL, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    connection, channel = message_queue_connect()

    tool = CountObjects(PICTURAS_YOLO_MODEL_PATH)
    request_msg_class = CountObjectsRequestMessage
    result_msg_class = CountObjectsResultMessage
    print(result_msg_class)
    message_processor = MessageProcessor(tool, request_msg_class, result_msg_class, channel)

    try:
        message_processor.start()
    except KeyboardInterrupt:
        message_processor.stop()
        
    connection.close()
