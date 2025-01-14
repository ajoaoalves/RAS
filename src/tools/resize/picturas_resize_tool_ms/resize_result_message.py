from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .resize_request_message import ResizeRequestMessage


class ResizeResultOutput(BaseModel):
    type: str
    imageURI: str


class ResizeResultMessage(ResultMessage[ResizeResultOutput]):

    def __init__(self, request: ResizeRequestMessage, tool_result: Any, exception: Exception, *args):
        super().__init__(request, tool_result, exception, *args)
        if exception is None:
            self.output = ResizeResultOutput(
                type="image",
                imageURI=request.parameters.outputImageURI,
            )
