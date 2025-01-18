from typing import Any

from pydantic import BaseModel

from .core.messages.result_message import ResultMessage
from .crop_request_message import CropRequestMessage


class CropResultOutput(BaseModel):
    type: str
    imageURI: str


class CropResultMessage(ResultMessage[CropResultOutput]):

    def __init__(
        self,
        request: CropRequestMessage,
        tool_result: Any,
        exception: Exception,
        *args
    ):
        super().__init__(request, tool_result, exception, *args)
        if exception is None:
            self.output = CropResultOutput(
                type="image",
                imageURI=request.parameters.outputImageURI,
            )
