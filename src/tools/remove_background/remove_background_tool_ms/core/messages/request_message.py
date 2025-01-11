from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

Parameters = TypeVar("P", bound=BaseModel)


class RequestMessage(BaseModel, Generic[Parameters]):
    messageId: str
    timestamp: datetime
    procedure: str
    parameters: Parameters
