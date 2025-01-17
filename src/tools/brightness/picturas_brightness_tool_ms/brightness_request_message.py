from pydantic import BaseModel

from .core.messages.request_message import RequestMessage


class BrightnessParameters(BaseModel):
    inputImageURI: str
    outputImageURI: str
    brightnessValue: float


BrightnessRequestMessage = RequestMessage[BrightnessParameters]
