import logging

from .config import PICTURAS_LOG_LEVEL, PICTURAS_YOLO_MODEL_PATH
from .core.message_processor import MessageProcessor
from .core.message_queue_setup import message_queue_connect
from .count_people_request_message import CountPeopleRequestMessage
from .count_people_result_message import CountPeopleResultMessage
from .count_people_tool import CountPeople

# Configuração de logging
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
logging.basicConfig(level=PICTURAS_LOG_LEVEL, format=LOG_FORMAT)

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
    connection, channel = message_queue_connect()

    tool = CountPeople(PICTURAS_YOLO_MODEL_PATH)
    request_msg_class = CountPeopleRequestMessage
    result_msg_class = CountPeopleResultMessage

    message_processor = MessageProcessor(tool, request_msg_class, result_msg_class, channel)

    try:
        message_processor.start()
    except KeyboardInterrupt:
        message_processor.stop()
        
    connection.close()
