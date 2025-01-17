from datetime import datetime
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

from .request_message import RequestMessage

T = TypeVar("T", bound=BaseModel)


class Metadata(BaseModel):
    processingTime: float
    microservice: str


class Error(BaseModel):
    code: str
    description: str


class ResultMessage(BaseModel, Generic[T]):
    messageId: str
    correlationId: str
    timestamp: datetime
    metadata: Metadata
    status: str
    output: Optional[T] = None
    error: Optional[Error] = None

    def __init__(
        self,
        request: RequestMessage,
        _tool_result: Any,
        exception: Exception,
        processing_time: float,
        microservice_name: str,
    ):
        super().__init__(
            messageId=f"completion-{request.messageId}",
            correlationId=request.messageId,
            timestamp=datetime.now().isoformat(),
            metadata=Metadata(
                processingTime=processing_time,
                microservice=microservice_name,
            ),
            status="success" if exception is None else "error",
            error=None if exception is None else Error(
                code=exception.__class__.__name__,
                description=str(exception),
            ),
        )
