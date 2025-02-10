from pydantic import BaseModel

from .core.messages.request_message import RequestMessage


class RemoveBackgroundParameters(BaseModel):
    inputImageURI: str
    outputImageURI: str

RemoveBackgroundRequestMessage = RequestMessage[RemoveBackgroundParameters]
