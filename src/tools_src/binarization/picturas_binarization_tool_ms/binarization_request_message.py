from pydantic import BaseModel

from .core.messages.request_message import RequestMessage


class BinarizationParameters(BaseModel):
    inputImageURI: str
    outputImageURI: str


BinarizationRequestMessage = RequestMessage[BinarizationParameters]
