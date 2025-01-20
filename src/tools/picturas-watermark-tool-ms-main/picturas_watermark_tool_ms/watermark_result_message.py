from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .watermark_request_message import WatermarkRequestMessage


class WatermarkResultOutput(BaseModel):
    type: str
    imageURI: str


class WatermarkResultMessage(ResultMessage[WatermarkResultOutput]):

    def __init__(self, request: WatermarkRequestMessage, tool_result: Any, exception: Exception, *args):
        super().__init__(request, tool_result, exception, *args)
        if exception is None:
            self.output = WatermarkResultOutput(
                type="image",
                imageURI=request.parameters.outputImageURI,
            )
