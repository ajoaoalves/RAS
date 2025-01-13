from pydantic import BaseModel

from .core.messages.request_message import RequestMessage

class RotateParameters(BaseModel):
    inputImageURI: str
    outputImageURI: str
    angle: int

RotateRequestMessage = RequestMessage[RotateParameters]