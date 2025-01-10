from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .border_request_message import BorderRequestMessage


class BorderResultOutput(BaseModel):
    type: str
    imageURI: str


class BorderResultMessage(ResultMessage[BorderResultOutput]):

    def __init__(self, request: BorderRequestMessage, tool_result: Any, exception: Exception, *args):
        super().__init__(request, tool_result, exception, *args)
        if exception is None:
            self.output = BorderResultOutput(
                type="image",
                imageURI=request.parameters.outputImageURI,
            )
