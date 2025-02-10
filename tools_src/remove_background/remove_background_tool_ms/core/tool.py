from abc import ABC, abstractmethod
from typing import Any

from .messages.request_message import Parameters


class Tool(ABC):

    @abstractmethod
    def apply(self, parameters: Parameters) -> Any:
        pass
