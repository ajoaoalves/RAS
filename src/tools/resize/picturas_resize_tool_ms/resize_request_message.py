from pydantic import BaseModel

from .core.messages.request_message import RequestMessage


class ResizeParameters(BaseModel):
    inputImageURI: str
    outputImageURI: str
    width: int
    height: int


ResizeRequestMessage = RequestMessage[ResizeParameters]
