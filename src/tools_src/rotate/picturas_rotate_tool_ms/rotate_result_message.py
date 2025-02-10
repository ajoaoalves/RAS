from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .rotate_request_message import RotateRequestMessage

class RotateResultOutput(BaseModel):
    type: str
    outputImageURI: str


class RotateResultMessage(ResultMessage[RotateResultOutput]):
    
    def __init__(self, request: RotateRequestMessage, tool_result: Any, exception: Exception, *args):
        super().__init__(request, tool_result, exception, *args)
        if exception is None:
            self.output = RotateResultOutput(
                type="image",
                outputImageURI=request.parameters.outputImageURI,
            )