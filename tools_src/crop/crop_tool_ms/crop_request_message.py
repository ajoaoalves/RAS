from pydantic import BaseModel
from .core.messages.request_message import RequestMessage


class cropParameters(BaseModel):
    inputImageURI: str
    outputImageURI: str
    crop_box: tuple  # A tuple (left, upper, right, lower) defining the crop region


CropRequestMessage = RequestMessage[cropParameters]
